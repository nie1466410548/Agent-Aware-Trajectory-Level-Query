import pandas as pd
import numpy as np

# Load events from snapshot changes
event_sql = """
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at, monthly_spend,
    CASE plan_name WHEN 'Starter' THEN 1 WHEN 'Growth' THEN 2 WHEN 'Scale' THEN 3 WHEN 'Enterprise' THEN 4 END AS tier
  FROM intercom__company_enhanced
),
ordered AS (
  SELECT *, LAG(tier) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_tier,
         LAG(plan_name) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_plan,
         LAG(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS prev_created_at,
         LEAD(created_at) OVER (PARTITION BY company_name ORDER BY created_at) AS next_created_at
  FROM tiers
)
SELECT company_name, created_at AS event_at, prev_created_at, next_created_at,
       prev_plan, plan_name AS new_plan, prev_tier, tier,
       CASE WHEN tier > prev_tier THEN 'upgrade' ELSE 'downgrade' END AS event_type
FROM ordered
WHERE prev_tier IS NOT NULL AND tier <> prev_tier
"""
events = db.frame(db.query(event_sql))
events['event_at'] = pd.to_datetime(events['event_at'])
events['prev_created_at'] = pd.to_datetime(events['prev_created_at'])
events['next_created_at'] = pd.to_datetime(events['next_created_at'])
print("Total events:", len(events))
print(events['event_type'].value_counts())

# Filter to companies with conversations
conv_companies = [
    "Acme Associates", "Apex Networks", "Cobalt Platforms", "Delta Software", 
    "Edge Industries", "Edge Platforms", "Fusion Insights", "Global Logistics", 
    "Global Technologies", "Harbor Systems", "Insight Logistics", "Insight Ventures", 
    "Keystone Analytics", "Keystone Group", "Keystone Technologies", "Lumina Collaborative", 
    "Lumina Industries", "Lumina Insights", "Momentum Advisors", "Nimbus Associates", 
    "Optima Advisors", "Pioneer Group", "Pioneer Services", "Quantum Platforms", 
    "River Analytics", "Summit Software", "Velocity Labs", "Zenith Platforms"
]

events_conv = events[events['company_name'].isin(conv_companies)].copy()
print(f"Events for companies with conversations: {len(events_conv)}")
print(events_conv['event_type'].value_counts())

# Load all conversations
conv_sql = """
SELECT all_contact_company_names as company_name, conversation_created_at, 
       all_conversation_tags, sla_status, conversation_initiated_type
FROM intercom__conversation_enhanced
"""
convs = db.frame(db.query(conv_sql))
convs['conversation_created_at'] = pd.to_datetime(convs['conversation_created_at'])
print("Conversations:", len(convs))

# For each event, find conversations in the PREVIOUS plan period (from prev_created_at to event_at)
# and the NEXT plan period (from event_at to next_created_at)
# If no prev_created_at, use the company's conversation min
# If no next_created_at, use the company's conversation max

records = []
for _, ev in events_conv.iterrows():
    cn = ev['company_name']
    sub = convs[convs['company_name'] == cn]
    if len(sub) == 0:
        continue
    cmin = sub['conversation_created_at'].min()
    cmax = sub['conversation_created_at'].max()
    
    evt = ev['event_at']
    prev_start = max(ev['prev_created_at'], cmin) if pd.notna(ev['prev_created_at']) else cmin
    next_end = min(ev['next_created_at'], cmax) if pd.notna(ev['next_created_at']) else cmax
    
    before = sub[(sub['conversation_created_at'] >= prev_start) & (sub['conversation_created_at'] < evt)]
    after = sub[(sub['conversation_created_at'] > evt) & (sub['conversation_created_at'] <= next_end)]
    
    if len(before) == 0 and len(after) == 0:
        continue
    
    def summarize(window_df):
        if len(window_df) == 0:
            return dict(convs=0, bugs=0, outages=0, escalations=0, sla=0, cust_init=0)
        return dict(
            convs=len(window_df),
            bugs=window_df['all_conversation_tags'].str.contains('Bug', na=False).sum(),
            outages=window_df['all_conversation_tags'].str.contains('Outage', na=False).sum(),
            escalations=window_df['all_conversation_tags'].str.contains('Escalation', na=False).sum(),
            sla=window_df['sla_status'].eq('breached').sum(),
            cust_init=window_df['conversation_initiated_type'].eq('customer_initiated').sum()
        )
    
    b = summarize(before)
    a = summarize(after)
    
    b_days = max((evt - prev_start).days, 0)
    a_days = max((next_end - evt).days, 0)
    
    rec = {'company_name': cn, 'event_at': evt, 'event_type': ev['event_type'],
           'prev_plan': ev['prev_plan'], 'new_plan': ev['new_plan'],
           'prev_period_start': prev_start, 'next_period_end': next_end}
    for k, v in b.items():
        rec[f'before_{k}'] = v
    rec['before_days'] = b_days
    for k, v in a.items():
        rec[f'after_{k}'] = v
    rec['after_days'] = a_days
    records.append(rec)

evdf = pd.DataFrame(records)
print(f"\nEvents with conversation data in plan periods: {len(evdf)}")
print(evdf['event_type'].value_counts())

# Compute rates
for p in ['before', 'after']:
    evdf[f'{p}_conv_rate'] = evdf[f'{p}_convs'] / evdf[f'{p}_days'].replace(0, 1)
    evdf[f'{p}_bug_rate'] = evdf[f'{p}_bugs'] / evdf[f'{p}_days'].replace(0, 1)
    evdf[f'{p}_outage_rate'] = evdf[f'{p}_outages'] / evdf[f'{p}_days'].replace(0, 1)
    evdf[f'{p}_sla_rate'] = evdf[f'{p}_sla'] / evdf[f'{p}_days'].replace(0, 1)

print("\n=== Summary by event type (full plan-period windows) ===")
for evt in ['upgrade', 'downgrade']:
    sub = evdf[evdf['event_type'] == evt]
    print(f"\n--- {evt.upper()} (n={len(sub)}) ---")
    print(f"  Before: {sub['before_convs'].sum():.0f} convs in {sub['before_days'].sum():.0f} days ({sub['before_conv_rate'].mean():.3f}/day avg)")
    print(f"  After:  {sub['after_convs'].sum():.0f} convs in {sub['after_days'].sum():.0f} days ({sub['after_conv_rate'].mean():.3f}/day avg)")
    print(f"  Bug rate: before={sub['before_bug_rate'].mean():.4f}, after={sub['after_bug_rate'].mean():.4f}")
    print(f"  Outage rate: before={sub['before_outage_rate'].mean():.4f}, after={sub['after_outage_rate'].mean():.4f}")
    print(f"  SLA breach rate: before={sub['before_sla_rate'].mean():.4f}, after={sub['after_sla_rate'].mean():.4f}")
    
    # Paired t-test
    from scipy import stats
    print(f"  Paired t-test (conv rate): t={stats.ttest_rel(sub['after_conv_rate'], sub['before_conv_rate'])[0]:.3f}, p={stats.ttest_rel(sub['after_conv_rate'], sub['before_conv_rate'])[1]:.4f}")
    print(f"  Paired t-test (bug rate): t={stats.ttest_rel(sub['after_bug_rate'], sub['before_bug_rate'])[0]:.3f}, p={stats.ttest_rel(sub['after_bug_rate'], sub['before_bug_rate'])[1]:.4f}")

evdf.to_csv('/work/plan_period_analysis.csv', index=False)
print("\nSaved to /work/plan_period_analysis.csv")