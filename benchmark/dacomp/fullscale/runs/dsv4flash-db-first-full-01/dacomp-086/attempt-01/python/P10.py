import pandas as pd
import numpy as np
df = pd.read_csv('/work/customer_health_scores.csv')

df['account_age_months'] = df['account_age_days']/30.44
df['monthly_won_rate'] = df['total_won_amount']/df['account_age_months'].clip(lower=1)
df['health_factor'] = df['health_score']/100.0
df['renewal_base'] = df['health_factor']*df['monthly_won_rate']*6
df['pipeline_upside'] = df['health_factor']*(df['win_rate_percentage']/100.0)*df['current_pipeline_amount']
df['predicted_6mo_revenue'] = df['renewal_base']+df['pipeline_upside']

print("Component contribution to total predicted revenue:")
print(f"  Renewal base total: ${df['renewal_base'].sum()/1e9:.1f}B ({df['renewal_base'].sum()/df['predicted_6mo_revenue'].sum()*100:.1f}%)")
print(f"  Pipeline upside total: ${df['pipeline_upside'].sum()/1e9:.1f}B ({df['pipeline_upside'].sum()/df['predicted_6mo_revenue'].sum()*100:.1f}%)")

top = df.nlargest(10, 'predicted_6mo_revenue')
print("\nTop 10 accounts by predicted 6-month contribution:")
print(top[['account_name','industry_normalized','account_size_segment','health_score','predicted_6mo_revenue','annual_revenue','current_pipeline_amount']].round(0).to_string(index=False))

risk = df[df['health_score']<50]
print(f"\nLow-health accounts (n={len(risk)}):")
print(f"  Pipeline at risk: ${risk['current_pipeline_amount'].sum()/1e9:.2f}B")
print(f"  Historical won amount at risk: ${risk['total_won_amount'].sum()/1e9:.2f}B")
print(f"  Predicted 6-mo contribution: ${risk['predicted_6mo_revenue'].sum()/1e9:.2f}B")

# For strategy: sizes within low health
print("\nLow health by size:")
print(risk['account_size_segment'].value_counts())

# Industry shares of low health
print("\nLow health by industry:")
print(risk['industry_normalized'].value_counts())