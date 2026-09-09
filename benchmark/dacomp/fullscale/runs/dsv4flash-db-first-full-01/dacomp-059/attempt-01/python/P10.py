import pandas as pd
import numpy as np
from scipy import stats

df_all = pd.read_csv('/work/df_all.csv')
df_all['is_problem'] = df_all['is_problem'].astype(int)

# Economics metrics
df_all['cpc'] = df_all['spend'] / df_all['clicks'].replace(0, np.nan)
df_all['cpa'] = df_all['spend'] / df_all['conversions'].replace(0, np.nan)
df_all['conv_value_per_conv'] = df_all['conversions_value'] / df_all['conversions'].replace(0, np.nan)  # need conversions_value in df
df_all['roas'] = df_all['conversions_value'] / df_all['spend'].replace(0, np.nan)

print("=== Economics by group (mean) ===")
eco = df_all.groupby('is_problem')[['cpc','cpa','roas','spend','clicks']].mean().round(3)
print(eco.to_string())

# I need conversions_value - reload from df_ag if missing
if 'conversions_value' not in df_all.columns:
    df_ag = pd.read_csv('/work/df_ag.csv')
    df_all = df_all.merge(df_ag[['ad_group_id','conversions']].rename(columns={'conversions':'conv_ag'}), on='ad_group_id', how='left', suffixes=('','_x'))
# Check
print("\nColumns:", [c for c in df_all.columns])

# Statistical tests
for metric in ['ctr','cvr','intent_match_index','traffic_quality_score']:
    a = df_all.loc[df_all['is_problem']==1, metric].dropna()
    b = df_all.loc[df_all['is_problem']==0, metric].dropna()
    stat, p = stats.mannwhitneyu(a, b, alternative='two-sided')
    print(f"{metric}: problem_med={a.median():.4f}, nonprob_med={b.median():.4f}, MWU p={p:.3e}")

# Channel x Strategy problem rates
df_all['channel_strategy'] = df_all['channel'] + ' / ' + df_all['strategy']
ct = df_all.groupby('channel_strategy').apply(
    lambda g: pd.Series({'total': len(g), 'problem': g['is_problem'].sum(),
                          'problem_pct': 100.0*g['is_problem'].mean()})).reset_index()
ct = ct.sort_values('problem_pct', ascending=False)
print("\n=== Channel x Strategy problem rates ===")
print(ct.round(1).to_string(index=False))