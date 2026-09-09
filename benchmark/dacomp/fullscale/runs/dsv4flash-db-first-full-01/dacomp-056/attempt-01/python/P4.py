import pandas as pd
import numpy as np
import scipy.stats as st
import json

# Load the archived dedup result from /results/S34.rows.jsonl
rows = []
with open('/results/S34.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows)
print("rows loaded:", df.shape)
print("columns:", df.columns.tolist())

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

# Composite RFM model
df['composite_rfm'] = 0.35*df['recency_score'] + 0.3*df['frequency_score'] + 0.35*df['monetary_score']

# Consistency metrics: std of R,F,M and M-RF gap
df['rfm_std'] = df[['recency_score','frequency_score','monetary_score']].std(axis=1)
df['m_rf_gap'] = df['monetary_score'] - (df['recency_score'] + df['frequency_score']) / 2

print("\n=== Consistency Metrics by Group ===")
print(df.groupby('customer_group')[['rfm_std','m_rf_gap','composite_rfm']].mean().round(4))

# T-test for monetary vs recency/frequency gap significance
hve = df[df['customer_group']=='HVE']
smb = df[df['customer_group']=='SMB']
print("\n=== T-test: M-RF gap (HVE vs SMB) ===")
t_stat, p_val = st.ttest_ind(hve['m_rf_gap'], smb['m_rf_gap'], equal_var=False)
print(f"t={t_stat:.4f}, p={p_val:.6e}")

print("\n=== T-test: LTV (HVE vs SMB) ===")
t_stat, p_val = st.ttest_ind(hve['estimated_customer_ltv'], smb['estimated_customer_ltv'], equal_var=False)
print(f"t={t_stat:.4f}, p={p_val:.6e}")

# Correlation: monetary vs recency/frequency
print("\n=== Correlation: recency vs monetary ===")
print(df.groupby('customer_group')[['recency_score','monetary_score']].corr().round(4))

# Check relationship between days_since_last_activity and recency_score
print("\n=== Correlation: days_since_last_activity vs recency_score ===")
print(df.groupby('customer_group')[['days_since_last_activity','recency_score']].corr().round(4))

# Value stability distribution
print("\n=== Value Stability Distribution ===")
print(pd.crosstab(df['customer_group'], df['value_stability'], normalize='index').round(3))

# Strategic classification
print("\n=== Strategic Classification ===")
print(pd.crosstab(df['customer_group'], df['strategic_classification'], normalize='index').round(3))

# Lifecycle stage
print("\n=== Lifecycle Stage ===")
print(pd.crosstab(df['customer_group'], df['lifecycle_stage'], normalize='index').round(3))

# Upsell potential
print("\n=== Upsell Potential ===")
print(pd.crosstab(df['customer_group'], df['upsell_potential'], normalize='index').round(3))

# Development opportunity
print("\n=== Development Opportunity ===")
print(pd.crosstab(df['customer_group'], df['development_opportunity'], normalize='index').round(3))

# Risk category
print("\n=== Risk Category ===")
print(pd.crosstab(df['customer_group'], df['risk_category'], normalize='index').round(3))