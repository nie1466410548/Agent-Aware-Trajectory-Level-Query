import pandas as pd
import numpy as np
import re

df_ag2 = pd.read_csv('/work/df_ag2.csv')
df_kw = pd.read_csv('/work/df_kw.csv')
df_kw['is_problem'] = df_kw['is_problem'].astype(int)

# Match type scores
mt_score = {'EXACT': 100, 'PHRASE': 75, 'BROAD_MATCH_MODIFIER': 50, 'BROAD': 25}

transactional = {"buy","cheap","price","discount","sale","delivery","warranty","purchase","order"}

def tokens(text):
    return set(re.findall(r'[a-z]+', str(text).lower()))

df_kw['tok'] = df_kw['keyword_text'].apply(tokens)
df_kw['has_transactional'] = df_kw['tok'].apply(lambda t: len(t & transactional) > 0)

# Per-ad-group: match type score (clicks-weighted) and transactional share
grp_kw = df_kw.groupby('ad_group_id').apply(lambda g: pd.Series({
    'mt_score': np.average([mt_score.get(m, 50) for m in g['keyword_match_type']], weights=g['clicks']) if g['clicks'].sum()>0 else 50,
    'trans_share': (g[g['has_transactional']]['clicks'].sum() / g['clicks'].sum()) if g['clicks'].sum()>0 else np.nan
})).reset_index()

df_all = df_ag2.merge(grp_kw, on='ad_group_id', how='left')

# For ad groups without keyword data, fill with overall medians
df_all['mt_score'] = df_all['mt_score'].fillna(df_all['mt_score'].median())
df_all['trans_share'] = df_all['trans_share'].fillna(df_all['trans_share'].median())

# Component A: Intent Match
df_all['score_A'] = np.clip(df_all['intent_match_index'].fillna(1.0) / 2.0, 0, 1) * 100
# Component B: Match type precision (already 0-100)
df_all['score_B'] = df_all['mt_score']
# Component C: Keyword intent alignment (trans share 0.5 => 100)
df_all['score_C'] = np.clip(df_all['trans_share'] / 0.5, 0, 1) * 100

df_all['traffic_quality_score'] = 0.4*df_all['score_A'] + 0.3*df_all['score_B'] + 0.3*df_all['score_C']

print("=== Traffic Quality Score by group ===")
print(df_all.groupby('is_problem')['traffic_quality_score'].describe().to_string())
print("\nComponent A (Intent Match) by group:")
print(df_all.groupby('is_problem')['score_A'].describe().to_string())
print("\nComponent B (Match type) by group:")
print(df_all.groupby('is_problem')['score_B'].describe().to_string())
print("\nComponent C (Keyword intent) by group:")
print(df_all.groupby('is_problem')['score_C'].describe().to_string())

df_all.to_csv('/work/df_all.csv', index=False)