import pandas as pd, numpy as np, json

# Load monthly trend data
rows = [json.loads(l) for l in open('/results/S49.rows.jsonl')]
trend_df = pd.DataFrame(rows)
print(trend_df.shape)
print(trend_df.head(15))
print('\nUnique accounts:', trend_df['account_id'].nunique())
print('Months range:', trend_df['month'].min(), '-', trend_df['month'].max())

# Pivot to see each account's monthly trend
for acc in ['ACC00000008', 'ACC00000006', 'ACC00000007', 'ACC00000004']:
    adf = trend_df[trend_df['account_id'] == acc].sort_values('month')
    print(f'\n{acc}:')
    print(adf[['month', 'month_minutes', 'month_events', 'month_visitors', 'month_active_days']].to_string(index=False))

trend_df.to_csv('/work/monthly_trends.csv', index=False)
print('\nsaved')