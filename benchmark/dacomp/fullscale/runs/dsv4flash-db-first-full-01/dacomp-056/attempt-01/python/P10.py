import pandas as pd
import numpy as np

df = pd.read_pickle('/work/analysis_data.pkl')
df['inactive_share'] = df['days_since_last_activity'] / df['account_age_days'].clip(lower=1)
df['active_share'] = 1 - df['inactive_share']

hve = df[df['customer_group']=='HVE'].copy()
smb = df[df['customer_group']=='SMB'].copy()

# SMB by tier
print("=== SMB by tier ===")
print(smb.groupby('customer_tier').agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_churn=('churn_probability','mean'),
    avg_health=('customer_health_score','mean'),
    avg_active_share=('active_share','mean')
).round(3))

# HVE: Retention/Maturity cluster
print("\n=== HVE: Maturity+Retention lifecycle ===")
sub = hve[hve['lifecycle_stage'].isin(['Maturity','Retention'])]
print(sub.groupby('lifecycle_stage').agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_churn=('churn_probability','mean'),
    avg_health=('customer_health_score','mean'),
    avg_m=('monetary_score','mean'),
    avg_inactive=('days_since_last_activity','mean'),
    avg_active_share=('active_share','mean')
).round(2))

# HVE: Dormant cluster
print("\n=== HVE: Dormant lifecycle ===")
sub = hve[hve['lifecycle_stage']=='Dormant']
print(sub[['marketo_lead_id','customer_tier','customer_segment','estimated_customer_ltv',
           'churn_probability','customer_health_score','days_since_last_activity',
           'account_age_days','active_share']].head(10))
print(f"Mean active_share for Dormant HVE: {sub['active_share'].mean():.3f}")

# Correlation: m_rf_gap vs LTV
print("\n=== Correlation: m_rf_gap vs LTV ===")
print(f"HVE: r = {hve['m_rf_gap'].corr(hve['estimated_customer_ltv']):.4f}")
print(f"SMB: r = {smb['m_rf_gap'].corr(smb['estimated_customer_ltv']):.4f}")

# HVE Champion vs Loyal vs Potential Loyalist
print("\n=== HVE Segment Detail ===")
for seg in hve['customer_segment'].unique():
    sub = hve[hve['customer_segment']==seg]
    print(f"\n  {seg} (n={len(sub)}):")
    print(f"    LTV: {sub['estimated_customer_ltv'].mean():.0f} | Health: {sub['customer_health_score'].mean():.2f} | Churn: {sub['churn_probability'].mean():.2f}")
    print(f"    R={sub['recency_score'].mean():.2f} F={sub['frequency_score'].mean():.2f} M={sub['monetary_score'].mean():.2f}")
    print(f"    M-RF gap: {sub['m_rf_gap'].mean():.3f} | rfm_std: {sub['rfm_std'].mean():.3f}")
    print(f"    Age: {sub['account_age_days'].mean():.0f}d | Inactive: {sub['days_since_last_activity'].mean():.0f}d | Active share: {sub['active_share'].mean():.3f}")
    print(f"    Value stability: {sub['value_stability'].value_counts().to_dict()}")
    print(f"    Risk: {sub['risk_category'].value_counts().to_dict()}")
    print(f"    Lifecycle: {sub['lifecycle_stage'].value_counts().to_dict()}")
    print(f"    Recommended model: {sub['recommended_engagement_model'].value_counts().to_dict()}")
    print(f"    Success target: {sub['success_target'].value_counts().to_dict()}")

# ===== Key summary statistics for report =====
print("\n\n===== KEY STATISTICS SUMMARY =====")
print(f"Total customers: {len(df)}")
print(f"HVE customers: {len(hve)} ({len(hve)/len(df)*100:.1f}%)")
print(f"SMB customers: {len(smb)} ({len(smb)/len(df)*100:.1f}%)")
print(f"\nHVE portfolio contribution: {hve['portfolio_contribution_pct'].sum()*100:.1f}% of total portfolio")
print(f"SMB portfolio contribution: {smb['portfolio_contribution_pct'].sum()*100:.1f}% of total portfolio")
print(f"\nHVE avg LTV: ${hve['estimated_customer_ltv'].mean():.0f}")
print(f"SMB avg LTV: ${smb['estimated_customer_ltv'].mean():.0f}")
print(f"HVE avg churn probability: {hve['churn_probability'].mean():.2f}")
print(f"SMB avg churn probability: {smb['churn_probability'].mean():.2f}")
print(f"\nHVE avg M-RF gap: {hve['m_rf_gap'].mean():.3f}")
print(f"SMB avg M-RF gap: {smb['m_rf_gap'].mean():.3f}")
print(f"\nHVE rfm_std (lower consistency): {hve['rfm_std'].mean():.3f}")
print(f"SMB rfm_std: {smb['rfm_std'].mean():.3f}")
print(f"\nHVE median active_share: {hve['active_share'].median():.3f}")
print(f"SMB median active_share: {smb['active_share'].median():.3f}")

# Concentration: top 10 HVE customers
top10 = hve.nlargest(10, 'portfolio_contribution_pct')
print(f"\nTop 10 HVE by portfolio contribution: {top10['portfolio_contribution_pct'].sum()*100:.1f}% of total portfolio")
print(f"These {len(top10)} customers contribute {top10['portfolio_contribution_pct'].sum()/df['portfolio_contribution_pct'].sum()*100:.1f}% of ALL portfolio")