import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

df = pd.read_pickle('/work/analysis_data.pkl')
hve = df[df['customer_group']=='HVE'].copy()
smb = df[df['customer_group']=='SMB'].copy()

# Time-based proxy: inactive share of account lifetime
df['inactive_share'] = df['days_since_last_activity'] / df['account_age_days'].clip(lower=1)
df['active_share'] = 1 - df['inactive_share']
print("=== Time-based efficiency proxy (share of account life with activity) ===")
print(df.groupby('customer_group')[['account_age_days','days_since_last_activity','active_share','inactive_share']].mean().round(3))

# Chi-square: lifecycle stage distribution
ct = pd.crosstab(df['customer_group'], df['lifecycle_stage'])
chi2, p, dof, _ = chi2_contingency(ct)
print(f"\nChi2 lifecycle stage: chi2={chi2:.1f}, p={p:.3e}")

ct = pd.crosstab(df['customer_group'], df['risk_category'])
chi2, p, dof, _ = chi2_contingency(ct)
print(f"Chi2 risk category: chi2={chi2:.1f}, p={p:.3e}")

ct = pd.crosstab(df['customer_group'], df['value_stability'])
chi2, p, dof, _ = chi2_contingency(ct)
print(f"Chi2 value stability: chi2={chi2:.1f}, p={p:.3e}")

# === Investment recommendation for HVE ===
print("\n=== HVE: Investment Recommendation ===")
print(hve.groupby('investment_recommendation').agg(n=('marketo_lead_id','count'),
      avg_ltv=('estimated_customer_ltv','mean'), avg_churn=('churn_probability','mean'),
      avg_health=('customer_health_score','mean')).round(2))

print("\n=== HVE: Acquisition ROI Assessment ===")
print(hve.groupby('acquisition_roi_assessment').agg(n=('marketo_lead_id','count'),
      avg_ltv=('estimated_customer_ltv','mean'), avg_churn=('churn_probability','mean')).round(2))

print("\n=== HVE: Success Target ===")
print(hve.groupby('success_target').agg(n=('marketo_lead_id','count'),
      avg_ltv=('estimated_customer_ltv','mean'), avg_churn=('churn_probability','mean'),
      avg_inactive=('days_since_last_activity','mean')).round(2))

print("\n=== HVE: rfm_segment ===")
print(hve.groupby('rfm_segment').agg(n=('marketo_lead_id','count'),
      avg_ltv=('estimated_customer_ltv','mean'), avg_health=('customer_health_score','mean')).round(2))

# === HVE Gold vs Platinum summary ===
print("\n=== HVE: Gold vs Platinum ===")
print(hve.groupby('customer_tier')[['estimated_customer_ltv','customer_health_score','churn_probability',
      'recency_score','frequency_score','monetary_score','account_age_days','days_since_last_activity',
      'investment_priority_score']].mean().round(2))

# === Segments of SMB for strategy design ===
print("\n=== SMB by tier ===")
print(smb.groupby('customer_tier').agg(n=('marketo_lead_id','count'),
      avg_ltv=('estimated_customer_ltv','mean'), avg_churn=('churn_probability','mean'),
      avg_health=('customer_health_score','mean'), avg_active_share=('active_share','mean')).round(3))

# === HVE: At-Risk / Retention focus cluster ===
print("\n=== HVE: Maturity+Retention lifecycle (at-risk of lapse) ===")
sub = hve[hve['lifecycle_stage'].isin(['Maturity','Retention'])]
print(sub.groupby('lifecycle_stage').agg(n=('marketo_lead_id','count'),
      avg_ltv=('estimated_customer_ltv','mean'), avg_churn=('churn_probability','mean'),
      avg_health=('customer_health_score','mean'), avg_m=('monetary_score','mean'),
      avg_inactive=('days_since_last_activity','mean')).round(2))

# === Consistency proxy validation: inactive share correlation with rfm_std ===
print("\n=== Correlation: rfm_std vs inactive_share (HVE) ===")
print(f"r = {hve['rfm_std'].corr(hve['inactive_share']):.4f}")
print("=== Correlation: m_rf_gap vs LTV (HVE) ===")
print(f"r = {hve['m_rf_gap'].corr(hve['estimated_customer_ltv']):.4f}")
print("=== Correlation: m_rf_gap vs LTV (SMB) ===")
print(f"r = {smb['m_rf_gap'].corr(smb['estimated_customer_ltv']):.4f}")
