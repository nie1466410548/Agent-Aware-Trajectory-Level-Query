import pandas as pd
import numpy as np
import json

# Column names from the table schema + rn
cols = ['marketo_lead_id', 'stripe_customer_id', 'zendesk_user_id', 'primary_email', 
        'primary_organization', 'customer_segment', 'customer_tier', 'rfm_segment', 'rfm_score',
        'rfm_avg_score', 'recency_score', 'frequency_score', 'monetary_score', 
        'estimated_customer_ltv', 'adjusted_ltv', 'expected_annual_revenue', 'revenue_tier',
        'strategic_classification', 'value_stability', 'upsell_potential', 'churn_probability',
        'potential_revenue_loss', 'revenue_risk_percentage', 'portfolio_contribution_pct',
        'concentration_risk', 'investment_priority_score', 'acquisition_roi_assessment',
        'recommended_engagement_model', 'investment_recommendation', 'success_target',
        'development_opportunity', 'customer_health_score', 'lifecycle_stage', 'risk_category',
        'account_age_days', 'days_since_last_activity', 'analysis_timestamp', 'rn']

rows = []
with open('/results/S34.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows, columns=cols)
print("Loaded:", df.shape)
print(df.columns.tolist())

# Define groups
df['customer_group'] = np.where(
    (df['customer_tier'].isin(['Gold','Platinum'])) & (df['portfolio_contribution_pct'] > 0.05),
    'HVE', 'SMB')
print(df['customer_group'].value_counts())

# Basic stats
num_cols = ['recency_score','frequency_score','monetary_score','rfm_avg_score',
      'estimated_customer_ltv','customer_health_score','churn_probability',
      'account_age_days','days_since_last_activity','portfolio_contribution_pct',
      'investment_priority_score']
print("\n=== Group Means ===")
print(df.groupby('customer_group')[num_cols].mean().round(3))

# Composite RFM
df['composite_rfm'] = 0.35*df['recency_score'] + 0.3*df['frequency_score'] + 0.35*df['monetary_score']

# Consistency metrics
df['rfm_std'] = df[['recency_score','frequency_score','monetary_score']].std(axis=1)
df['m_rf_gap'] = df['monetary_score'] - (df['recency_score'] + df['frequency_score']) / 2

print("\n=== Consistency Metrics by Group ===")
print(df.groupby('customer_group')[['rfm_std','m_rf_gap','composite_rfm']].mean().round(4))

# T-tests
import scipy.stats as st
hve = df[df['customer_group']=='HVE']
smb = df[df['customer_group']=='SMB']
print("\n=== T-test: M-RF gap (HVE vs SMB) ===")
t, p = st.ttest_ind(hve['m_rf_gap'], smb['m_rf_gap'], equal_var=False)
print(f"t={t:.4f}, p={p:.6e}")

print("\n=== T-test: LTV (HVE vs SMB) ===")
t, p = st.ttest_ind(hve['estimated_customer_ltv'], smb['estimated_customer_ltv'], equal_var=False)
print(f"t={t:.4f}, p={p:.6e}")

# Distributions
print("\n=== Value Stability ===")
print(pd.crosstab(df['customer_group'], df['value_stability'], normalize='index').round(3))

print("\n=== Strategic Classification ===")
print(pd.crosstab(df['customer_group'], df['strategic_classification'], normalize='index').round(3))

print("\n=== Lifecycle Stage ===")
print(pd.crosstab(df['customer_group'], df['lifecycle_stage'], normalize='index').round(3))

print("\n=== Upsell Potential ===")
print(pd.crosstab(df['customer_group'], df['upsell_potential'], normalize='index').round(3))

print("\n=== Development Opportunity ===")
print(pd.crosstab(df['customer_group'], df['development_opportunity'], normalize='index').round(3))

print("\n=== Risk Category ===")
print(pd.crosstab(df['customer_group'], df['risk_category'], normalize='index').round(3))

print("\n=== Customer Segment ===")
print(pd.crosstab(df['customer_group'], df['customer_segment'], normalize='index').round(3))

# Correlation: monetary vs recency
print("\n=== Correlation (recency, monetary) by group ===")
for grp in ['HVE','SMB']:
    sub = df[df['customer_group']==grp]
    print(f"{grp}: r(recency, monetary)={sub['recency_score'].corr(sub['monetary_score']):.4f}")
    print(f"{grp}: r(frequency, monetary)={sub['frequency_score'].corr(sub['monetary_score']):.4f}")

# Save a copy for visualization
df.to_pickle('/work/analysis_data.pkl')
print("\nData saved to /work/analysis_data.pkl")