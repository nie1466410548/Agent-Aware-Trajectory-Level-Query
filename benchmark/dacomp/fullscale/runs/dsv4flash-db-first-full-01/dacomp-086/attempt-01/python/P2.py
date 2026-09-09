import numpy as np
import pandas as pd

df = db.frame(db.query("SELECT account_id, days_since_last_activity, total_activities_30d, total_contacts, contacts_with_email, annual_revenue, total_won_amount, account_size_segment, number_of_employees, account_age_days, win_rate_percentage, current_pipeline_amount, industry_normalized FROM salesforce__customer_360_view"))

for col in ['days_since_last_activity', 'total_activities_30d', 'number_of_employees', 'annual_revenue', 'total_won_amount', 'account_age_days', 'win_rate_percentage']:
    s = df[col]
    print(f"{col}: min={s.min():.3f}, p10={s.quantile(0.10):.3f}, p25={s.quantile(0.25):.3f}, p50={s.quantile(0.50):.3f}, p75={s.quantile(0.75):.3f}, p90={s.quantile(0.90):.3f}, max={s.max():.3f}")

print("\nlog10 annual_revenue: min=%.3f max=%.3f" % (np.log10(df['annual_revenue']).min(), np.log10(df['annual_revenue']).max()))
print("log10(total_won_amount+1): min=%.3f max=%.3f" % (np.log10(df['total_won_amount']+1).min(), np.log10(df['total_won_amount']+1).max()))
print("log10(number_of_employees): min=%.3f max=%.3f" % (np.log10(df['number_of_employees']).min(), np.log10(df['number_of_employees']).max()))
print("total_won_amount zeros:", (df['total_won_amount']==0).sum())

print("\nCorrelation of days_since_last_activity with activities_30d:", df['days_since_last_activity'].corr(df['total_activities_30d']))
print("Correlation annual_revenue with total_won:", df['annual_revenue'].corr(df['total_won_amount']))
print("win_rate_percentage nulls:", df['win_rate_percentage'].isna().sum(), "min:", df['win_rate_percentage'].min(), "max:", df['win_rate_percentage'].max())