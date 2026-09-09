import pandas as pd
import numpy as np
import scipy.stats as st
import json

# Load the archived dedup result from S34
rows = []
with open('results/S34.rows.jsonl') as f:
    for line in f:
        rows.append(json.loads(line))
df = pd.DataFrame(rows)
print("rows loaded:", df.shape)
print(df.columns.tolist())

# Define groups
df['customer_group'] = np.where(
    (df['customer_tier'].isin(['Gold','Platinum'])) & (df['portfolio_contribution_pct'] > 0.05),
    'HVE', 'SMB')
print(df['customer_group'].value_counts())

# Basic numeric overview
print(df.groupby('customer_group')[['recency_score','frequency_score','monetary_score','rfm_avg_score',
      'estimated_customer_ltv','customer_health_score','churn_probability',
      'account_age_days','days_since_last_activity']].mean().round(3))

# Composite RFM (own model): weighted RFM = 0.35R+0.3F+0.35M
df['composite_rfm'] = 0.35*df['recency_score'] + 0.3*df['frequency_score'] + 0.35*df['monetary_score']
# Spread / consistency metric: std of R,F,M per customer (higher = less consistent)
df['rfm_std'] = df[['recency_score','frequency_score','monetary_score']].std(axis=1)
df['rfm_cv'] = df['rfm_std'] / df[['recency_score','frequency_score','monetary_score']].mean(axis=1)
# Monetary minus engagement avg (M - (R+F)/2) as "value-engagement gap"
df['m_rf_gap'] = df['monetary_score'] - (df['recency_score']+df['frequency_score'])/2

print("\nConsistency metrics by group:")
print(df.groupby('customer_group')[['rfm_std','rfm_cv','m_rf_gap','composite_rfm']].mean().round(4))
