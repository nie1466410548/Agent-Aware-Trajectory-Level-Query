import pandas as pd
import numpy as np

df_kw = pd.read_csv('/work/df_kw.csv')
df_kw['is_problem'] = df_kw['is_problem'].astype(int)

# Match type distribution within problem vs non-problem (clicks-weighted)
mt = df_kw.groupby(['is_problem','keyword_match_type']).agg(
    clicks=('clicks','sum'), conv=('conversions','sum'), spend=('spend','sum')).reset_index()
mt['cvr_pct'] = 100.0*mt['conv']/mt['clicks'].replace(0, np.nan)
mt['click_share_pct'] = mt.groupby('is_problem')['clicks'].apply(lambda x: 100.0*x/x.sum()).reset_index(drop=True)
print("=== Match type distribution by group ===")
print(mt.round(2).to_string(index=False))

# Keyword match type in problem groups: share of ad groups using each type
ag_mt = df_kw.groupby(['ad_group_id','is_problem','keyword_match_type']).size().reset_index('keyword_match_type')
ag_mt_count = df_kw.groupby(['ad_group_id','is_problem']).agg(types=('keyword_match_type', lambda x: list(set(x)))).reset_index()
print("\nMatch type combinations in problem groups:")
problem_combos = ag_mt_count[ag_mt_count['is_problem']==1]['types'].apply(lambda x: tuple(sorted(x))).value_counts()
print(problem_combos.head(10))

# Non-problem
non_prob_combos = ag_mt_count[ag_mt_count['is_problem']==0]['types'].apply(lambda x: tuple(sorted(x))).value_counts()
print("\nMatch type combinations in non-problem groups (top 5):")
print(non_prob_combos.head(5))

# Keyword-broad-only problem groups analysis
broad_only = ag_mt_count[ag_mt_count['is_problem']==1][ag_mt_count[ag_mt_count['is_problem']==1]['types'].apply(lambda x: list(x)==['BROAD'])]
print(f"\nProblem groups with ONLY BROAD match type: {len(broad_only)}")
print(f"Problem groups with ONLY EXACT match type: {len(ag_mt_count[(ag_mt_count['is_problem']==1) & (ag_mt_count['types'].apply(lambda x: list(x)==['EXACT']))])}")