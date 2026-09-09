import pandas as pd
df = pd.read_csv('/work/customer_health_scores.csv')

# Revenue tier thresholds (quintile boundaries)
q = df['predicted_6mo_revenue'].quantile([0, 0.2, 0.4, 0.6, 0.8, 1.0])
print("Revenue tier thresholds:")
for i in range(5):
    lo, hi = q.iloc[i], q.iloc[i+1]
    n = df[(df['predicted_6mo_revenue']>=lo) & (df['predicted_6mo_revenue']<=hi)].shape[0]
    print(f"  Tier {5-i}: ${lo:,.0f} - ${hi:,.0f}  (n={n})")

# Pipeline vs won relationship
print("\nPipeline-to-won ratio (median):", (df['current_pipeline_amount']/df['total_won_amount'].replace(0,np.nan)).median())

# Model component share
df['account_age_months'] = df['account_age_days']/30.44
df['monthly_won_rate'] = df['total_won_amount']/df['account_age_months'].clip(lower=1)
df['health_factor'] = df['health_score']/100.0
df['renewal_base'] = df['health_factor']*df['monthly_won_rate']*6
df['pipeline_upside'] = df['health_factor']*(df['win_rate_percentage']/100.0)*df['current_pipeline_amount']
df['predicted_6mo_revenue'] = df['renewal_base']+df['pipeline_upside']

print("\nComponent contribution to total predicted revenue:")
print(f"  Renewal base total: ${df['renewal_base'].sum()/1e9:.1f}B ({df['renewal_base'].sum()/df['predicted_6mo_revenue'].sum()*100:.1f}%)")
print(f"  Pipeline upside total: ${df['pipeline_upside'].sum()/1e9:.1f}B ({df['pipeline_upside'].sum()/df['predicted_6mo_revenue'].sum()*100:.1f}%)")

# Top 10 accounts by predicted revenue
top = df.nlargest(10, 'predicted_6mo_revenue')
print("\nTop 10 accounts by predicted 6-month contribution:")
print(top[['account_name','industry_normalized','account_size_segment','health_score','predicted_6mo_revenue','annual_revenue','current_pipeline_amount']].round(0).to_string(index=False))

# Low health risk concentration: pipeline at risk
risk = df[df['health_score']<50]
print(f"\nPipeline at risk in Low-health accounts: ${risk['current_pipeline_amount'].sum()/1e9:.2f}B")
print(f"Won revenue at risk: ${risk['total_won_amount'].sum()/1e9:.2f}B")