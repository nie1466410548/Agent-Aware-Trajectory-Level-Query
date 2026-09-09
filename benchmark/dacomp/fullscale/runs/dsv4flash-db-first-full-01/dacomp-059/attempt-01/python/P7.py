import pandas as pd
import numpy as np

df_ag = pd.read_csv('/work/df_ag.csv')
df_kw = pd.read_csv('/work/df_kw.csv')
df_kw['is_problem'] = df_kw['is_problem'].astype(int)

# ---- Benchmark CVR per (industry, keyword) from keyword report ----
df_kw['kw_cvr'] = df_kw['conversions'] / df_kw['clicks'].replace(0, np.nan)
bench = df_kw.groupby(['industry', 'keyword_text']).agg(
    kw_clicks=('clicks', 'sum'), kw_conv=('conversions', 'sum')).reset_index()
bench['bench_cvr'] = bench['kw_conv'] / bench['kw_clicks'].replace(0, np.nan)

# Merge keyword rows with benchmark, then compute leave-one-out expected CVR per ad group
df_kw_m = df_kw.merge(bench, on=['industry', 'keyword_text'], how='left')

# Leave-one-out: for each ad group, subtract its own keyword clicks/conv from the benchmark pool
exp_rows = []
for ag_id, grp in df_kw_m.groupby('ad_group_id'):
    tot = grp.groupby('keyword_text').agg(c=('clicks','sum'), conv=('conversions','sum')).reset_index()
    # benchmark without own contribution
    bsub = bench[bench['keyword_text'].isin(tot['keyword_text'])]
    merged = tot.merge(bsub, on='keyword_text')
    merged['pool_clicks'] = merged['kw_clicks'] - merged['c']
    merged['pool_conv'] = merged['kw_conv'] - merged['conv']
    merged['loo_cvr'] = merged['pool_conv'] / merged['pool_clicks'].replace(0, np.nan)
    # weighted expected CVR by the ad group's own keyword clicks
    w = merged['c']
    exp_cvr = np.average(merged['loo_cvr'], weights=w) if w.sum() > 0 and merged['loo_cvr'].notna().any() else np.nan
    exp_rows.append({'ad_group_id': ag_id, 'expected_cvr': exp_cvr})

exp_df = pd.DataFrame(exp_rows)
df_ag2 = df_ag.merge(exp_df, on='ad_group_id', how='left')
df_ag2['intent_match_index'] = df_ag2['cvr'] / df_ag2['expected_cvr'].replace(0, np.nan)

print("=== Intent Match Index by group ===")
print(df_ag2.groupby('is_problem')['intent_match_index'].agg(['count','mean','median','min','max']).round(3).to_string())
print("\nExpected CVR by group:")
print(df_ag2.groupby('is_problem')['expected_cvr'].agg(['count','mean','median']).round(4).to_string())
print("\nActual CVR by group:")
print(df_ag2.groupby('is_problem')['cvr'].agg(['count','mean','median']).round(4).to_string())

df_ag2.to_csv('/work/df_ag2.csv', index=False)