import pandas as pd
import numpy as np
import json
from collections import Counter

# Load search term data
cols_st = ['ad_group_id', 'search_term', 'keyword_match_type', 'search_term_match_type', 's_impressions', 's_clicks', 's_spend', 's_conversions']
st = pd.DataFrame([json.loads(l) for l in open('/results/S22.rows.jsonl')], columns=cols_st)

# Load all ad groups
cols_ag = ['ad_group_id', 'ad_group_name', 'campaign_id', 'campaign_name', 'account_name', 'status',
           'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S16.rows.jsonl')], columns=cols_ag)

ctr_p75 = np.percentile(ag['ctr'], 75)
cvr_p25 = np.percentile(ag['cvr'], 25)
ag['is_problematic'] = (ag['ctr'] > ctr_p75) & (ag['cvr'] < cvr_p25)
prob_ids = set(ag[ag['is_problematic']]['ad_group_id'])

# Search term analysis
st['is_problematic'] = st['ad_group_id'].isin(prob_ids)
print("Search term analysis:")
print(f"Problematic ad groups with search terms: {st[st['is_problematic']]['ad_group_id'].nunique()}")
print(f"Total search term rows: {len(st)}, Problematic: {st['is_problematic'].sum()}")

# Search term match type distribution
print("\n--- Search term match type distribution (by impressions) ---")
st_match = st.groupby(['is_problematic', 'search_term_match_type']).agg(
    imps=('s_impressions', 'sum'), clks=('s_clicks', 'sum'), conv=('s_conversions', 'sum')
).reset_index()
for prob in [True, False]:
    subset = st_match[st_match['is_problematic'] == prob]
    total = subset['imps'].sum()
    print(f"\n{'PROBLEMATIC' if prob else 'NON-PROBLEMATIC'} (total imps={total:.0f}):")
    for _, r in subset.iterrows():
        ctr = r['clks']/r['imps'] if r['imps']>0 else 0
        cvr = r['conv']/r['clks'] if r['clks']>0 else 0
        print(f"  {r['search_term_match_type']:<20} imp={r['imps']:>8.0f} ({r['imps']/total*100:5.1f}%)  clk={r['clks']:>6.0f}  CTR={ctr:.4f}  CVR={cvr:.4f}")

# Also by keyword match type in search terms
print("\n--- Search term keyword match type distribution ---")
st_kw = st.groupby(['is_problematic', 'keyword_match_type']).agg(
    imps=('s_impressions', 'sum'), clks=('s_clicks', 'sum'), conv=('s_conversions', 'sum')
).reset_index()
for prob in [True, False]:
    subset = st_kw[st_kw['is_problematic'] == prob]
    total = subset['imps'].sum()
    print(f"\n{'PROBLEMATIC' if prob else 'NON-PROBLEMATIC'}:")
    for _, r in subset.iterrows():
        ctr = r['clks']/r['imps'] if r['imps']>0 else 0
        cvr = r['conv']/r['clks'] if r['clks']>0 else 0
        print(f"  {r['keyword_match_type']:<25} imp={r['imps']:>8.0f} ({r['imps']/total*100:5.1f}%)  clk={r['clks']:>6.0f}  CTR={ctr:.4f}  CVR={cvr:.4f}")

# Top search terms in problematic groups
print("\n--- Top 30 search terms by impressions in PROBLEMATIC ad groups ---")
st_prob = st[st['is_problematic']]
st_top = st_prob.groupby('search_term').agg(
    imps=('s_impressions', 'sum'), clks=('s_clicks', 'sum'), conv=('s_conversions', 'sum'),
    n_adgroups=('ad_group_id', 'nunique')
).sort_values('imps', ascending=False).head(30)
st_top['ctr'] = st_top['clks'] / st_top['imps']
st_top['cvr'] = st_top['conv'] / st_top['clks'].replace(0, np.nan)
print(st_top.to_string())

# Compare with non-problematic
print("\n--- Top 30 search terms by impressions in NON-PROBLEMATIC ad groups ---")
st_nonprob = st[~st['is_problematic']]
st_top_np = st_nonprob.groupby('search_term').agg(
    imps=('s_impressions', 'sum'), clks=('s_clicks', 'sum'), conv=('s_conversions', 'sum'),
    n_adgroups=('ad_group_id', 'nunique')
).sort_values('imps', ascending=False).head(30)
st_top_np['ctr'] = st_top_np['clks'] / st_top_np['imps']
st_top_np['cvr'] = st_top_np['conv'] / st_top_np['clks'].replace(0, np.nan)
print(st_top_np.to_string())