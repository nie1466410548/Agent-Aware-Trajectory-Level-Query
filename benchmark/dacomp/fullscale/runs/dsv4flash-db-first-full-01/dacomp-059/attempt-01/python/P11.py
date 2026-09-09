import pandas as pd
import numpy as np
from scipy import stats

df_all = pd.read_csv('/work/df_all.csv')
df_all['is_problem'] = df_all['is_problem'].astype(int)

# Need conversions_value - get from original query
result = db.query("""
    SELECT ad_group_id, SUM(conversions_value) AS conv_value, SUM(conversions) AS conv
    FROM google_ads__ad_group_report
    GROUP BY ad_group_id
    HAVING SUM(clicks) > 0 AND SUM(impressions) > 0
""")
e = result['executions'][0]
rows = db.rows(result)
df_extra = pd.DataFrame(rows, columns=e['columns'])
df_all = df_all.merge(df_extra, on='ad_group_id', how='left')

# Economics metrics
df_all['cpc'] = df_all['spend'] / df_all['clicks'].replace(0, np.nan)
df_all['cpa'] = df_all['spend'] / df_all['conv'].replace(0, np.nan)
df_all['conv_value_per_conv'] = df_all['conv_value'] / df_all['conv'].replace(0, np.nan)
df_all['roas'] = df_all['conv_value'] / df_all['spend'].replace(0, np.nan)

print("=== Economics by group (mean) ===")
eco = df_all.groupby('is_problem')[['cpc','cpa','roas','spend','clicks','conv']].mean().round(3)
print(eco.to_string())

# Statistical tests
print("\n=== Statistical Tests (Mann-Whitney U) ===")
for metric in ['ctr','cvr','intent_match_index','traffic_quality_score']:
    a = df_all.loc[df_all['is_problem']==1, metric].dropna()
    b = df_all.loc[df_all['is_problem']==0, metric].dropna()
    stat, p = stats.mannwhitneyu(a, b, alternative='two-sided')
    print(f"{metric}: problem_med={a.median():.4f}, non_prob_med={b.median():.4f}, MWU p={p:.3e}")

# Channel x Strategy problem rates
df_all['channel_strategy'] = df_all['channel'] + ' / ' + df_all['strategy']
ct = df_all.groupby('channel_strategy').apply(
    lambda g: pd.Series({'total': len(g), 'problem': int(g['is_problem'].sum()),
                          'problem_pct': round(100.0*g['is_problem'].mean(),1)})).reset_index()
ct = ct.sort_values('problem_pct', ascending=False)
print("\n=== Channel x Strategy problem rates ===")
print(ct.to_string(index=False))

# Save
df_all.to_csv('/work/df_all.csv', index=False)