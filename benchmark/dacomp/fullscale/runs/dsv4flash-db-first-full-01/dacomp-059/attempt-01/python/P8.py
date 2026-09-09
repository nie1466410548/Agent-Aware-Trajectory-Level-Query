import pandas as pd
import numpy as np

df_ag = pd.read_csv('/work/df_ag.csv')
df_kw = pd.read_csv('/work/df_kw.csv')
df_kw['is_problem'] = df_kw['is_problem'].astype(int)

# How many ad groups have keyword data?
ag_with_kw = df_kw['ad_group_id'].unique()
print(f"Ad groups with keyword data: {len(ag_with_kw)}")
print(f"Problem ad groups with keyword data: {len(set(df_ag[df_ag['is_problem']==1]['ad_group_id']) & set(ag_with_kw))}")
print(f"Non-problem ad groups with keyword data: {len(set(df_ag[df_ag['is_problem']==0]['ad_group_id']) & set(ag_with_kw))}")

# Let me check the number of industry-keyword combos
bench = df_kw.groupby(['industry', 'keyword_text']).agg(
    kw_clicks=('clicks', 'sum'), kw_conv=('conversions', 'sum')).reset_index()
bench['bench_cvr'] = bench['kw_conv'] / bench['kw_clicks'].replace(0, np.nan)
print(f"Industry-keyword combos: {len(bench)}")
print(f"Combos with NaN bench_cvr (zero clicks): {bench['bench_cvr'].isna().sum()}")

# Check how many problem ad groups have keywords that match to benchmark
df_kw_m = df_kw.merge(bench, on=['industry', 'keyword_text'], how='left')
print(f"Keyword rows after merge: {len(df_kw_m)}, NaN bench_cvr: {df_kw_m['bench_cvr'].isna().sum()}")

# Let me just compute a simpler expected CVR: for each ad group, 
# expected CVR = avg of its keywords' industry-benchmark CVRs weighted by clicks
# Use all data (without leave-one-out) for simplicity and wider coverage
df_kw_m['exp_cvr_kw'] = df_kw_m['bench_cvr']  # benchmark per keyword

# Group by ad group: weighted average of keyword benchmark CVRs
ag_exp = df_kw_m.groupby('ad_group_id').apply(
    lambda g: np.average(g['exp_cvr_kw'], weights=g['clicks']) if g['exp_cvr_kw'].notna().any() and g['clicks'].sum()>0 else np.nan
).reset_index()
ag_exp.columns = ['ad_group_id', 'expected_cvr']

df_ag2 = df_ag.merge(ag_exp, on='ad_group_id', how='left')
df_ag2['intent_match_index'] = df_ag2['cvr'] / df_ag2['expected_cvr'].replace(0, np.nan)

print(f"\nAd groups with IMI: {df_ag2['intent_match_index'].notna().sum()}")
print(f"Problem groups with IMI: {df_ag2[df_ag2['is_problem']==1]['intent_match_index'].notna().sum()}")
print(f"Non-problem groups with IMI: {df_ag2[df_ag2['is_problem']==0]['intent_match_index'].notna().sum()}")

print("\n=== Intent Match Index by group ===")
print(df_ag2.groupby('is_problem')['intent_match_index'].describe().to_string())
print("\nExpected CVR by group:")
print(df_ag2.groupby('is_problem')['expected_cvr'].describe().to_string())

df_ag2.to_csv('/work/df_ag2.csv', index=False)