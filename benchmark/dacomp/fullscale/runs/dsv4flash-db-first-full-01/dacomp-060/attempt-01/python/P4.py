import pandas as pd
import numpy as np
import json

cols = ['ad_group_id', 'ad_group_name', 'campaign_name', 'account_name', 'status',
        'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']

rows = []
with open('/results/S11.rows.jsonl', 'r') as f:
    for line in f:
        rows.append(json.loads(line))

df = pd.DataFrame(rows, columns=cols)
print(f"Total ad groups: {len(df)}")
print(f"CTR range: {df['ctr'].min():.6f} - {df['ctr'].max():.6f}")
print(f"CVR range: {df['cvr'].min():.6f} - {df['cvr'].max():.6f}")

ctr_p75 = np.percentile(df['ctr'], 75)
cvr_p25 = np.percentile(df['cvr'], 25)
print(f"\nCTR 75th percentile: {ctr_p75:.6f}")
print(f"CVR 25th percentile: {cvr_p25:.6f}")

problematic = df[(df['ctr'] > ctr_p75) & (df['cvr'] < cvr_p25)].copy()
print(f"\nProblematic ad groups: {len(problematic)} out of {len(df)} ({len(problematic)/len(df)*100:.2f}%)")
problematic.to_csv('/work/problematic_ad_groups.csv', index=False)
print("\nProblematic ad group IDs:")
print(problematic['ad_group_id'].tolist())

# Display summary stats for problematic vs non-problematic
df['is_problematic'] = (df['ctr'] > ctr_p75) & (df['cvr'] < cvr_p25)
print("\n--- Problematic summary ---")
print(problematic[['ad_group_id', 'campaign_name', 'account_name', 'status', 'ctr', 'cvr', 'impressions', 'clicks', 'conversions']].to_string())