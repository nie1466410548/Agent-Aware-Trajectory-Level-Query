import pandas as pd, numpy as np

# Get monthly trend data via db interface
result = db.query("""
SELECT v.account_id,
       substr(dm.date_day, 1, 7) AS month,
       SUM(dm.sum_minutes) AS month_minutes,
       SUM(dm.sum_events) AS month_events,
       COUNT(DISTINCT dm.visitor_id) AS month_visitors,
       COUNT(DISTINCT dm.date_day) AS month_active_days
FROM pendo__visitor_daily_metrics dm
JOIN pendo__visitor v ON dm.visitor_id = v.visitor_id
GROUP BY v.account_id, substr(dm.date_day, 1, 7)
ORDER BY v.account_id, month
""")
trend_df = db.frame(result)
print('Shape:', trend_df.shape)
print('Accounts:', trend_df['account_id'].nunique())
print('Months:', trend_df['month'].min(), '-', trend_df['month'].max())

# Show detail for key accounts
for acc in ['ACC00000008', 'ACC00000006', 'ACC00000007', 'ACC00000004', 'ACC00000009']:
    adf = trend_df[trend_df['account_id'] == acc].sort_values('month')
    print(f'\n{acc} ({len(adf)} months):')
    print(adf[['month','month_minutes','month_events','month_visitors','month_active_days']].to_string(index=False))

print('\nTotal accounts with monthly data:')
for acc in trend_df['account_id'].unique():
    adf = trend_df[trend_df['account_id'] == acc].sort_values('month')
    print(f'  {acc}: {len(adf)} months, {adf["month"].min()} to {adf["month"].max()}')

trend_df.to_csv('/work/monthly_trends.csv', index=False)
print('saved')