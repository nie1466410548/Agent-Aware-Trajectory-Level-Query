import pandas as pd
import numpy as np
from scipy import stats

# Load conversations (no join)
sql1 = """
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type, conversation_id
FROM intercom__conversation_enhanced
"""
convs = db.frame(db.query(sql1))
convs['conversation_created_at'] = pd.to_datetime(convs['conversation_created_at'])
print("Conversations:", convs.shape)

# Load metrics
sql2 = """
SELECT conversation_id, count_total_parts, time_to_first_response_minutes, conversation_rating
FROM intercom__conversation_metrics
"""
metrics = db.frame(db.query(sql2))
print("Metrics:", metrics.shape)

# Merge
convs = convs.merge(metrics, on='conversation_id', how='left')
print("Merged:", convs.shape)

# Load events
event_sql = """
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_plan, plan_name AS new_plan,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier
"""
events = db.frame(db.query(event_sql))
events['event_at'] = pd.to_datetime(events['event_at'])
print("Events:", events.shape)
print(events['event_type'].value_counts())

# Per-event window analysis
records = []
for _, ev in events.iterrows():
    cn = ev['company_name']
    evt = ev['event_at']
    sub = convs[convs['company_name'] == cn].copy()
    
    before = sub[(sub['conversation_created_at'] < evt) & (sub['conversation_created_at'] >= evt - pd.Timedelta(days=30))]
    after = sub[(sub['conversation_created_at'] > evt) & (sub['conversation_created_at'] <= evt + pd.Timedelta(days=30))]
    
    def summarize(window_df):
        if len(window_df) == 0:
            return dict(convs=0, parts=0, bugs=0, outages=0, escalations=0, sla=0, cust_init=0, rating=0)
        return dict(
            convs=len(window_df),
            parts=window_df['count_total_parts'].sum(),
            bugs=window_df['all_conversation_tags'].str.contains('Bug', na=False).sum(),
            outages=window_df['all_conversation_tags'].str.contains('Outage', na=False).sum(),
            escalations=window_df['all_conversation_tags'].str.contains('Escalation', na=False).sum(),
            sla=window_df['sla_status'].eq('breached').sum(),
            cust_init=window_df['conversation_initiated_type'].eq('customer_initiated').sum(),
            rating=window_df[window_df['conversation_rating']>0]['conversation_rating'].mean() if (window_df['conversation_rating']>0).any() else 0
        )
    
    b = summarize(before)
    a = summarize(after)
    
    # days observed
    cmin = sub['conversation_created_at'].min()
    cmax = sub['conversation_created_at'].max()
    if pd.isna(cmin) or pd.isna(cmax):
        b_days = 0
        a_days = 0
    else:
        b_days = max((evt - max(cmin, evt - pd.Timedelta(days=30))).days, 0)
        a_days = max((min(cmax, evt + pd.Timedelta(days=30)) - evt).days, 0)
    
    rec = {'company_name': cn, 'event_at': evt, 'event_type': ev['event_type'],
           'prev_plan': ev['prev_plan'], 'new_plan': ev['new_plan']}
    for k, v in b.items():
        rec[f'before_{k}'] = v
    rec['before_days'] = b_days
    for k, v in a.items():
        rec[f'after_{k}'] = v
    rec['after_days'] = a_days
    records.append(rec)

evdf = pd.DataFrame(records)

# Filter to events with at least 1 conversation in the window
mask = (evdf['before_convs'] + evdf['after_convs'] > 0)
print(f"\nEvents with data in window: {mask.sum()} / {len(evdf)}")
evdf_filt = evdf[mask].copy()
print(evdf_filt['event_type'].value_counts())

# Compute per-day intensities
for p in ['before', 'after']:
    evdf_filt[f'{p}_conv_rate'] = evdf_filt[f'{p}_convs'] / evdf_filt[f'{p}_days'].replace(0, 1)
    evdf_filt[f'{p}_bug_rate'] = evdf_filt[f'{p}_bugs'] / evdf_filt[f'{p}_days'].replace(0, 1)
    evdf_filt[f'{p}_outage_rate'] = evdf_filt[f'{p}_outages'] / evdf_filt[f'{p}_days'].replace(0, 1)
    evdf_filt[f'{p}_sla_rate'] = evdf_filt[f'{p}_sla'] / evdf_filt[f'{p}_days'].replace(0, 1)

evdf_filt['conv_rate_delta'] = evdf_filt['after_conv_rate'] - evdf_filt['before_conv_rate']
evdf_filt['bug_rate_delta'] = evdf_filt['after_bug_rate'] - evdf_filt['before_bug_rate']
evdf_filt['outage_rate_delta'] = evdf_filt['after_outage_rate'] - evdf_filt['before_outage_rate']
evdf_filt['sla_rate_delta'] = evdf_filt['after_sla_rate'] - evdf_filt['before_sla_rate']

print("\n=== Summary: Per-Event Metrics (30-day windows) ===")
for evt in ['upgrade', 'downgrade']:
    sub = evdf_filt[evdf_filt['event_type'] == evt]
    print(f"\n--- {evt.upper()} (n={len(sub)}) ---")
    print(f"  Before: convs={sub['before_convs'].sum():.0f}, days={sub['before_days'].sum():.0f}, rate={sub['before_conv_rate'].mean():.3f}/day")
    print(f"  After:  convs={sub['after_convs'].sum():.0f}, days={sub['after_days'].sum():.0f}, rate={sub['after_conv_rate'].mean():.3f}/day")
    print(f"  Bug rate: before={sub['before_bug_rate'].mean():.3f}, after={sub['after_bug_rate'].mean():.3f}")
    print(f"  Outage rate: before={sub['before_outage_rate'].mean():.3f}, after={sub['after_outage_rate'].mean():.3f}")
    print(f"  SLA breach rate: before={sub['before_sla_rate'].mean():.3f}, after={sub['after_sla_rate'].mean():.3f}")
    print(f"  Avg rating: before={sub['before_rating'].mean():.2f}, after={sub['after_rating'].mean():.2f}")
    print(f"  Avg daily conv rate: before={sub['before_conv_rate'].mean():.3f}, after={sub['after_conv_rate'].mean():.3f}")

# Statistical tests
print("\n=== Statistical Tests ===")
for evt in ['upgrade', 'downgrade']:
    sub = evdf_filt[evdf_filt['event_type'] == evt]
    print(f"\n--- {evt.upper()} Paired t-test (after vs before) ---")
    for col, label in [('conv_rate', 'Conversation rate'), ('bug_rate', 'Bug rate'), 
                       ('outage_rate', 'Outage rate'), ('sla_rate', 'SLA breach rate')]:
        b = sub[f'before_{col}'].values
        a = sub[f'after_{col}'].values
        if len(b) > 1:
            t, p = stats.ttest_rel(a, b)
            print(f"  {label}: before={b.mean():.4f}, after={a.mean():.4f}, t={t:.3f}, p={p:.4f}")

# Between-group comparison
print("\n=== Between-group (upgrade vs downgrade) deltas ===")
up = evdf_filt[evdf_filt['event_type']=='upgrade']
dn = evdf_filt[evdf_filt['event_type']=='downgrade']
for col, label in [('conv_rate_delta', 'Conv rate delta'), ('bug_rate_delta', 'Bug rate delta'),
                   ('outage_rate_delta', 'Outage rate delta'), ('sla_rate_delta', 'SLA breach rate delta')]:
    t, p = stats.ttest_ind(up[col].values, dn[col].values, equal_var=False)
    print(f"  {label}: upgrade={up[col].mean():.4f}, downgrade={dn[col].mean():.4f}, t={t:.3f}, p={p:.4f}")

# Save
evdf_filt.to_csv('/work/event_analysis.csv', index=False)
print("\nSaved to /work/event_analysis.csv")