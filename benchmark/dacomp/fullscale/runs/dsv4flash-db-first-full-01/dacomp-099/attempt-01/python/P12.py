import pandas as pd
import numpy as np
from scipy import stats

# Load the plan-period analysis
evdf = pd.read_csv('/work/plan_period_analysis.csv')

# Load company metrics (no updated_at in metrics table)
metrics_sql = """
SELECT ce.company_name, ce.plan_name, ce.monthly_spend, ce.user_count, ce.session_count,
       cm.total_conversations, cm.avg_conversation_rating, cm.p50_time_to_first_response_min,
       cm.p50_reopens, cm.registration_retention_7d, cm.registration_retention_30d,
       cm.contacts_active_7d, cm.contacts_active_30d, cm.contacts_total
FROM intercom__company_enhanced ce
JOIN intercom__company_metrics cm ON ce.company_id = cm.company_id
"""
company_data = db.frame(db.query(metrics_sql))
print("Company metrics shape:", company_data.shape)

# Aggregate to company level (mean per company name)
company_agg = company_data.groupby('company_name').agg({
    'monthly_spend': 'mean', 'user_count': 'mean', 'session_count': 'mean',
    'total_conversations': 'mean', 'avg_conversation_rating': 'mean',
    'p50_time_to_first_response_min': 'mean', 'p50_reopens': 'mean',
    'registration_retention_7d': 'mean', 'registration_retention_30d': 'mean',
    'contacts_active_7d': 'mean', 'contacts_active_30d': 'mean', 'contacts_total': 'mean'
}).reset_index()

evdf_merged = evdf.merge(company_agg, on='company_name', how='left')
print("Merged:", evdf_merged.shape)

# Also merge plan characteristics: the plan being upgraded FROM / downgraded FROM
# and the plan being moved TO
print("\n=== Company characteristics comparison (before-event state) ===")
print(f"Upgrade events: {len(evdf_merged[evdf_merged['event_type']=='upgrade'])}")
print(f"Downgrade events: {len(evdf_merged[evdf_merged['event_type']=='downgrade'])}")
for col in ['monthly_spend', 'user_count', 'session_count', 'total_conversations', 
            'avg_conversation_rating', 'p50_time_to_first_response_min', 'p50_reopens',
            'registration_retention_7d', 'registration_retention_30d',
            'contacts_active_7d', 'contacts_active_30d', 'contacts_total']:
    up_vals = evdf_merged[evdf_merged['event_type']=='upgrade'][col].dropna()
    dn_vals = evdf_merged[evdf_merged['event_type']=='downgrade'][col].dropna()
    if len(up_vals) > 1 and len(dn_vals) > 1:
        t, p = stats.ttest_ind(up_vals, dn_vals, equal_var=False)
        print(f"  {col}: upgrade={up_vals.mean():.2f}, downgrade={dn_vals.mean():.2f}, t={t:.3f}, p={p:.4f}")

# Transition matrix: from plan -> to plan for upgrades and downgrades
print("\n=== Plan transition patterns ===")
up = evdf_merged[evdf_merged['event_type']=='upgrade']
dn = evdf_merged[evdf_merged['event_type']=='downgrade']
print("\nUpgrade transitions:")
print(up.groupby(['prev_plan','new_plan']).size())
print("\nDowngrade transitions:")
print(dn.groupby(['prev_plan','new_plan']).size())

# Pre-event incident intensity: does a high rate of issues precede downgrades?
print("\n=== Pre-event characteristics by direction (means) ===")
for evt in ['upgrade', 'downgrade']:
    sub = evdf_merged[evdf_merged['event_type']==evt]
    print(f"\n--- {evt.upper()} (n={len(sub)}) ---")
    print(f"  Avg before conv rate: {sub['before_conv_rate'].mean():.3f}")
    print(f"  Avg before bug rate:  {sub['before_bug_rate'].mean():.3f}")
    print(f"  Avg before outage rate: {sub['before_outage_rate'].mean():.3f}")
    print(f"  Avg before SLA breach rate: {sub['before_sla_rate'].mean():.3f}")
    print(f"  Avg company monthly_spend: {sub['monthly_spend'].mean():.0f}")
    print(f"  Avg company user_count: {sub['user_count'].mean():.0f}")
    print(f"  Avg company session_count: {sub['session_count'].mean():.0f}")
    print(f"  Avg response time (min): {sub['p50_time_to_first_response_min'].mean():.1f}")
    print(f"  Avg rating: {sub['avg_conversation_rating'].mean():.2f}")

# What about ratio of incidents to total conversations?
for evt in ['upgrade', 'downgrade']:
    sub = evdf_merged[evdf_merged['event_type']==evt]
    bug_ratio = sub['before_bugs'].sum() / sub['before_convs'].sum()
    outage_ratio = sub['before_outages'].sum() / sub['before_convs'].sum()
    sla_ratio = sub['before_sla'].sum() / sub['before_convs'].sum()
    print(f"\n{evt.upper()} before-event incident ratios (incidents per conversation):")
    print(f"  Bug ratio: {bug_ratio:.3f}, Outage ratio: {outage_ratio:.3f}, SLA breach ratio: {sla_ratio:.3f}")