import pandas as pd
import numpy as np
from scipy import stats

sql = """
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
),
events AS (
  SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan, prev_tier, tier,
         CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
    AND company_name IN (SELECT DISTINCT all_contact_company_names FROM intercom__conversation_enhanced)
),
event_metrics AS (
  SELECT e.company_name, e.event_at, e.event_type, e.prev_plan, e.new_plan,
         c.conversation_id, c.conversation_created_at,
         CASE WHEN c.conversation_created_at < e.event_at THEN 'before' ELSE 'after' END AS period,
         cm.count_total_parts,
         CASE WHEN c.all_conversation_tags LIKE '%Bug%' THEN 1 ELSE 0 END AS is_bug,
         CASE WHEN c.all_conversation_tags LIKE '%Outage%' THEN 1 ELSE 0 END AS is_outage,
         CASE WHEN c.all_conversation_tags LIKE '%Escalation%' THEN 1 ELSE 0 END AS is_escalation,
         CASE WHEN c.all_conversation_tags LIKE '%Renewal%' THEN 1 ELSE 0 END AS is_renewal,
         CASE WHEN c.sla_status = 'breached' THEN 1 ELSE 0 END AS is_sla_breach,
         CASE WHEN c.conversation_initiated_type = 'customer_initiated' THEN 1 ELSE 0 END AS is_customer_initiated,
         c.conversation_rating
  FROM events e
  JOIN intercom__conversation_enhanced c ON c.all_contact_company_names = e.company_name
  LEFT JOIN intercom__conversation_metrics cm ON cm.conversation_id = c.conversation_id
  WHERE c.conversation_created_at >= datetime(e.event_at, '-30 days')
    AND c.conversation_created_at <= datetime(e.event_at, '+30 days')
    AND c.conversation_created_at != e.event_at
)
SELECT * FROM event_metrics
ORDER BY company_name, event_at, conversation_created_at
"""
df = db.frame(db.query(sql))
print("Shape:", df.shape)

df['event_key'] = df['company_name'] + '_' + df['event_at'].astype(str)

agg_cols = {
    'conversation_id': 'count',
    'count_total_parts': 'sum',
    'is_bug': 'sum',
    'is_outage': 'sum',
    'is_escalation': 'sum',
    'is_renewal': 'sum',
    'is_sla_breach': 'sum',
    'is_customer_initiated': 'sum',
    'conversation_rating': lambda x: x[x > 0].mean() if (x > 0).any() else 0
}

per_event = df.groupby(['event_key', 'company_name', 'event_at', 'event_type', 'prev_plan', 'new_plan', 'period']).agg(agg_cols).reset_index()
per_event.columns = ['event_key', 'company_name', 'event_at', 'event_type', 'prev_plan', 'new_plan', 'period', 'conv_count', 'total_parts', 'bug_count', 'outage_count', 'escalation_count', 'renewal_count', 'sla_breach_count', 'customer_initiated_count', 'avg_rating']

pivot = per_event.pivot_table(index=['event_key', 'company_name', 'event_at', 'event_type', 'prev_plan', 'new_plan'],
                              columns='period',
                              values=['conv_count', 'total_parts', 'bug_count', 'outage_count', 'escalation_count', 'renewal_count', 'sla_breach_count', 'customer_initiated_count', 'avg_rating'],
                              aggfunc='first').fillna(0)

pivot.columns = [f'{col[1]}_{col[0]}' for col in pivot.columns]
pivot = pivot.reset_index()

pivot['conv_delta'] = pivot['after_conv_count'] - pivot['before_conv_count']
pivot['parts_delta'] = pivot['after_total_parts'] - pivot['before_total_parts']
pivot['bug_delta'] = pivot['after_bug_count'] - pivot['before_bug_count']
pivot['outage_delta'] = pivot['after_outage_count'] - pivot['before_outage_count']
pivot['escalation_delta'] = pivot['after_escalation_count'] - pivot['before_escalation_count']
pivot['sla_breach_delta'] = pivot['after_sla_breach_count'] - pivot['before_sla_breach_count']
pivot['conv_change_pct'] = np.where(pivot['before_conv_count'] > 0,
                                     (pivot['after_conv_count'] - pivot['before_conv_count']) / pivot['before_conv_count'] * 100,
                                     np.where(pivot['after_conv_count'] > 0, 100, 0))

print(f"Total events: {len(pivot)}, upgrades: {(pivot['event_type']=='upgrade').sum()}, downgrades: {(pivot['event_type']=='downgrade').sum()}")

print("\n=== Average per-event metrics (30-day windows) ===")
for evt_type in ['upgrade', 'downgrade']:
    sub = pivot[pivot['event_type'] == evt_type]
    print(f"\n--- {evt_type.upper()} events (n={len(sub)}) ---")
    print(f"  Avg convs before: {sub['before_conv_count'].mean():.2f} | after: {sub['after_conv_count'].mean():.2f} | delta: {sub['conv_delta'].mean():.2f} | %change: {sub['conv_change_pct'].mean():.1f}%")
    print(f"  Avg parts before: {sub['before_total_parts'].mean():.2f} | after: {sub['after_total_parts'].mean():.2f}")
    print(f"  Avg bug before:   {sub['before_bug_count'].mean():.2f} | after: {sub['after_bug_count'].mean():.2f}")
    print(f"  Avg outage before:{sub['before_outage_count'].mean():.2f} | after: {sub['after_outage_count'].mean():.2f}")
    print(f"  Avg escalation before: {sub['before_escalation_count'].mean():.2f} | after: {sub['after_escalation_count'].mean():.2f}")
    print(f"  Avg SLA breach before: {sub['before_sla_breach_count'].mean():.2f} | after: {sub['after_sla_breach_count'].mean():.2f}")
    print(f"  Avg rating before: {sub['before_avg_rating'].mean():.2f} | after: {sub['after_avg_rating'].mean():.2f}")
    print(f"  Avg cust-initiated before: {sub['before_customer_initiated_count'].mean():.2f} | after: {sub['after_customer_initiated_count'].mean():.2f}")

print("\n=== Paired t-tests (after vs before) ===")
for evt_type in ['upgrade', 'downgrade']:
    sub = pivot[pivot['event_type'] == evt_type]
    print(f"\n--- {evt_type.upper()} ---")
    pairs = [('before_conv_count','after_conv_count','Conversations'),
             ('before_total_parts','after_total_parts','Parts'),
             ('before_bug_count','after_bug_count','Bugs'),
             ('before_outage_count','after_outage_count','Outages'),
             ('before_escalation_count','after_escalation_count','Escalations'),
             ('before_sla_breach_count','after_sla_breach_count','SLA breaches'),
             ('before_customer_initiated_count','after_customer_initiated_count','Customer-initiated')]
    for b, a, label in pairs:
        before = sub[b].values.astype(float)
        after = sub[a].values.astype(float)
        t_stat, p_val = stats.ttest_rel(after, before)
        print(f"  {label}: before={before.mean():.2f}, after={after.mean():.2f}, t={t_stat:.3f}, p={p_val:.4f}")

# Also compare upgrade vs downgrade events directly (independent t-tests on deltas)
print("\n=== Between-group tests (upgrade vs downgrade deltas) ===")
up = pivot[pivot['event_type']=='upgrade']
dn = pivot[pivot['event_type']=='downgrade']
for col, label in [('conv_delta','Conversation delta'), ('parts_delta','Parts delta'),
                   ('bug_delta','Bug delta'), ('outage_delta','Outage delta'),
                   ('escalation_delta','Escalation delta'), ('sla_breach_delta','SLA breach delta'),
                   ('conv_change_pct','Conv % change')]:
    t_stat, p_val = stats.ttest_ind(up[col].values.astype(float), dn[col].values.astype(float), equal_var=False)
    print(f"  {label}: upgrade={up[col].mean():.2f}, downgrade={dn[col].mean():.2f}, t={t_stat:.3f}, p={p_val:.4f}")

# Save the pivot for later use
pivot.to_csv('/work/pivot_events.csv', index=False)
print("\nSaved pivot to /work/pivot_events.csv")