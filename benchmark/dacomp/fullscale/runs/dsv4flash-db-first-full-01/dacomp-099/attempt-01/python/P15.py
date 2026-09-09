import pandas as pd
import numpy as np
from scipy import stats

# Load conversation data and compute company-level baseline rates
conv_sql = """
SELECT all_contact_company_names as company_name, conversation_created_at
FROM intercom__conversation_enhanced
"""
convs = db.frame(db.query(conv_sql))
convs['conversation_created_at'] = pd.to_datetime(convs['conversation_created_at'])

# Company baseline: overall conversation rate over full observed history
base = convs.groupby('company_name').agg(
    n_convs=('conversation_created_at', 'count'),
    min_t=('conversation_created_at', 'min'),
    max_t=('conversation_created_at', 'max')
).reset_index()
base['span_days'] = (base['max_t'] - base['min_t']).dt.days.clip(lower=1)
base['baseline_rate'] = base['n_convs'] / base['span_days']
print("=== Company baselines ===")
print(base.sort_values('n_convs', ascending=False).head(10).to_string())

# Load event windows (30-day analysis) - from earlier saved file
ev30 = pd.read_csv('/work/event_analysis.csv')
print("\n30-day window events:", ev30.shape)
print(ev30['event_type'].value_counts())

# Merge baseline into the 30-day events
ev30 = ev30.merge(base[['company_name', 'baseline_rate']], on='company_name', how='left')
# Compute ratio of before/after rate to baseline
for p in ['before', 'after']:
    ev30[f'{p}_rate'] = ev30[f'{p}_convs'] / ev30[f'{p}_days'].replace(0, 1)
    ev30[f'{p}_ratio'] = ev30[f'{p}_rate'] / ev30['baseline_rate'].replace(0, np.nan)

print("\n=== 30-day window events: rate relative to baseline ===")
print(ev30[['company_name','event_type','before_days','after_days','before_convs','after_convs','before_rate','after_rate','baseline_rate','before_ratio','after_ratio']].round(3).to_string())

# Overall findings for the report
print("\n=== Final consolidated numbers ===")
print("\nA) 30-day strict window (10 events):")
for evt in ['upgrade', 'downgrade']:
    sub = ev30[ev30['event_type'] == evt]
    print(f"  {evt}: before convs total={sub['before_convs'].sum()}, after convs total={sub['after_convs'].sum()}")
    print(f"        before bug={sub['before_bugs'].sum()}, after bug={sub['after_bugs'].sum()}")
    print(f"        before outage={sub['before_outages'].sum()}, after outage={sub['after_outages'].sum()}")
    print(f"        before sla={sub['before_sla'].sum()}, after sla={sub['after_sla'].sum()}")

print("\nB) Full plan-period windows (33 events):")
for evt in ['upgrade', 'downgrade']:
    sub = evdf2 if False else None

# Load plan period analysis
evp = pd.read_csv('/work/plan_period_analysis.csv')
for evt in ['upgrade', 'downgrade']:
    sub = evp[evp['event_type'] == evt]
    print(f"  {evt} (n={len(sub)}):")
    print(f"    before conv rate={sub['before_conv_rate'].mean():.3f}/day, after={sub['after_conv_rate'].mean():.3f}/day")
    print(f"    before bug rate={sub['before_bug_rate'].mean():.3f}/day, after={sub['after_bug_rate'].mean():.3f}/day")
    print(f"    before outage rate={sub['before_outage_rate'].mean():.3f}/day, after={sub['after_outage_rate'].mean():.3f}/day")
    print(f"    before sla rate={sub['before_sla_rate'].mean():.3f}/day, after={sub['after_sla_rate'].mean():.3f}/day")
    print(f"    before days total={sub['before_days'].sum()}, after days total={sub['after_days'].sum()}")
    print(f"    before convs total={sub['before_convs'].sum()}, after convs total={sub['after_convs'].sum()}")

# Customer-level view: net direction per company
print("\n=== Net plan direction per company (from snapshot history) ===")
event_sql = """
WITH tiers AS (
  SELECT company_id, company_name, plan_name, created_at,
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
         CASE WHEN tier > prev_tier THEN 1 ELSE -1 END AS delta
  FROM ordered
  WHERE prev_tier IS NOT NULL AND tier <> prev_tier
)
SELECT company_name, SUM(delta) AS net_direction, COUNT(*) as n_changes
FROM events
GROUP BY company_name
"""
net = db.frame(db.query(event_sql))
print(net.sort_values('net_direction').to_string())