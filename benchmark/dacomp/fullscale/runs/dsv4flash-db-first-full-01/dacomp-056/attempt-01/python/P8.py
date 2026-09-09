import pandas as pd
import numpy as np

df = pd.read_pickle('/work/analysis_data.pkl')
hve = df[df['customer_group']=='HVE'].copy()

print("=== HVE by Tier & Segment ===")
print(hve.groupby(['customer_tier','customer_segment']).agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_health=('customer_health_score','mean'),
    avg_churn=('churn_probability','mean'),
    avg_rfm=('composite_rfm','mean'),
    avg_r=('recency_score','mean'),
    avg_f=('frequency_score','mean'),
    avg_m=('monetary_score','mean'),
    avg_age=('account_age_days','mean'),
    avg_inactive=('days_since_last_activity','mean'),
    avg_portfolio=('portfolio_contribution_pct','mean')
).round(2))

print("\n=== HVE by Lifecycle ===")
print(hve.groupby('lifecycle_stage').agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_health=('customer_health_score','mean'),
    avg_churn=('churn_probability','mean'),
    avg_r=('recency_score','mean'),
    avg_m=('monetary_score','mean'),
    avg_inactive=('days_since_last_activity','mean')
).round(2))

print("\n=== HVE by Risk Category ===")
print(hve.groupby('risk_category').agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_health=('customer_health_score','mean'),
    avg_churn=('churn_probability','mean'),
    avg_m=('monetary_score','mean'),
    avg_inactive=('days_since_last_activity','mean')
).round(2))

print("\n=== HVE by Value Stability ===")
print(hve.groupby('value_stability').agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_health=('customer_health_score','mean'),
    avg_churn=('churn_probability','mean'),
    avg_m=('monetary_score','mean')
).round(2))

print("\n=== HVE by Recommended Engagement Model ===")
print(hve.groupby('recommended_engagement_model').agg(
    n=('marketo_lead_id','count'),
    avg_ltv=('estimated_customer_ltv','mean'),
    avg_health=('customer_health_score','mean'),
    avg_churn=('churn_probability','mean')
).round(2))

# ===== Define strategy quadrants =====
# Value axis: composite RFM; Risk axis: churn_probability
hve['value_band'] = pd.cut(hve['composite_rfm'], bins=[0, 3.9, 4.2, 5.01], labels=['Lower RFM','Mid RFM','High RFM'])
hve['risk_band'] = pd.cut(hve['churn_probability'], bins=[0, 0.3, 0.45, 0.6, 1.01], labels=['Low risk','Med risk','High risk','Very high risk'])
print("\n=== HVE Value x Risk Quadrant Matrix ===")
q = hve.pivot_table(index='risk_band', columns='value_band', values='marketo_lead_id', aggfunc='count', fill_value=0)
print(q)
print("\nLTV by quadrant:")
q_ltv = hve.pivot_table(index='risk_band', columns='value_band', values='estimated_customer_ltv', aggfunc='mean', fill_value=0)
print(q_ltv.round(0))

# Portfolio concentration - total contribution
print("\n=== Portfolio contribution (sum) by group ===")
print(df.groupby('customer_group')['portfolio_contribution_pct'].agg(['sum','mean','max']).round(4))

# Potential revenue loss
print("\n=== Potential Revenue Loss ===")
print(df.groupby('customer_group')['potential_revenue_loss'].agg(['sum','mean']).round(2))

# Average health/churn by customer_segment for HVE
print("\n=== HVE Champion vs Loyal vs Potential Loyalist ===")
print(hve.groupby('customer_segment')[['estimated_customer_ltv','customer_health_score','churn_probability',
      'recency_score','frequency_score','monetary_score','account_age_days','days_since_last_activity']].agg(
      ['mean','count']).round(2))
