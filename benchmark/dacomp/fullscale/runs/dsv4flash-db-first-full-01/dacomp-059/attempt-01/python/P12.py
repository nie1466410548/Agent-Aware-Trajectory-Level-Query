import pandas as pd
import numpy as np

df_all = pd.read_csv('/work/df_all.csv')
df_all['is_problem'] = df_all['is_problem'].astype(int)

# Period analysis for problem groups
period_stats = df_all.groupby('period').apply(lambda g: pd.Series({
    'total': len(g),
    'problem': int(g['is_problem'].sum()),
    'problem_pct': round(100.0*g['is_problem'].mean(),1),
    'ctr_pct': round(100.0*g['ctr'].mean(),3),
    'cvr_pct': round(100.0*g['cvr'].mean(),3),
    'median_imi': round(g['intent_match_index'].median(),2),
    'median_tqs': round(g['traffic_quality_score'].median(),1)
})).reset_index().sort_values('problem_pct', ascending=False)
print("=== Problem rates by campaign period ===")
print(period_stats.to_string(index=False))

# Quarter vs season grouping
def period_group(p):
    if p.startswith('Q'): return 'Quarter (' + p.split(' ')[0] + ' ' + p.split(' ')[1] + ')'
    return 'Season (' + p.split(' ')[0] + ' ' + p.split(' ')[1] + ')'
df_all['period_cat'] = df_all['period'].apply(period_group)
pg = df_all.groupby('period_cat').apply(lambda g: pd.Series({
    'total': len(g), 'problem': int(g['is_problem'].sum()),
    'problem_pct': round(100.0*g['is_problem'].mean(),1)})).reset_index()
print("\n=== Quarter vs Season problem rates ===")
print(pg.to_string(index=False))

# Top spend problem ad groups
top = df_all[df_all['is_problem']==1].sort_values('spend', ascending=False).head(15)
print("\n=== Top-spend problem ad groups ===")
print(top[['ad_group_id','channel','strategy','industry','clicks','ctr','cvr','spend','intent_match_index','traffic_quality_score']].round(4).to_string(index=False))