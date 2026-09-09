import pandas as pd
import numpy as np
import json

# Load all ad group data
cols_ag = ['ad_group_id', 'ad_group_name', 'campaign_id', 'campaign_name', 'account_name', 'status',
           'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S16.rows.jsonl')], columns=cols_ag)

# Load keyword data (S18 problematic, S21 all)
# S21: ad_group_id, keyword_match_type, type, kw_status, kw_impressions, kw_clicks, kw_spend, kw_conversions
cols_kw = ['ad_group_id', 'keyword_match_type', 'type', 'kw_status', 'kw_impressions', 'kw_clicks', 'kw_spend', 'kw_conversions']
kw = pd.DataFrame([json.loads(l) for l in open('/results/S21.rows.jsonl')], columns=cols_kw)

# S18: keywords for problematic
cols_kw18 = ['ad_group_id', 'keyword_text', 'keyword_match_type', 'type', 'kw_status', 'kw_impressions', 'kw_clicks', 'kw_spend', 'kw_conversions']
kw18 = pd.DataFrame([json.loads(l) for l in open('/results/S18.rows.jsonl')], columns=cols_kw18)

# Flag problematic
ctr_p75 = np.percentile(ag['ctr'], 75)
cvr_p25 = np.percentile(ag['cvr'], 25)
ag['is_problematic'] = (ag['ctr'] > ctr_p75) & (ag['cvr'] < cvr_p25)

prob_ids = set(ag[ag['is_problematic']]['ad_group_id'])
print(f"Problematic ad group IDs in keyword report: {len(prob_ids & set(kw['ad_group_id']))}")
print(f"Problematic ad groups total: {len(prob_ids)}")

# Keyword match type distribution - compare problematic vs non-problematic
kw['is_problematic'] = kw['ad_group_id'].isin(prob_ids)
kw_agg = kw.groupby(['is_problematic', 'keyword_match_type']).agg(
    kw_impressions=('kw_impressions', 'sum'),
    kw_clicks=('kw_clicks', 'sum'),
    kw_spend=('kw_spend', 'sum'),
    kw_conversions=('kw_conversions', 'sum')
).reset_index()

print("\n--- Keyword match type distribution ---")
for prob in [True, False]:
    subset = kw_agg[kw_agg['is_problematic'] == prob]
    total_imp = subset['kw_impressions'].sum()
    total_clk = subset['kw_clicks'].sum()
    total_conv = subset['kw_conversions'].sum()
    print(f"\n{'PROBLEMATIC' if prob else 'NON-PROBLEMATIC'} (total imps={total_imp:.0f}, clicks={total_clk:.0f}, conv={total_conv:.1f}):")
    for _, r in subset.iterrows():
        ctr = r['kw_clicks']/r['kw_impressions'] if r['kw_impressions']>0 else 0
        cvr = r['kw_conversions']/r['kw_clicks'] if r['kw_clicks']>0 else 0
        print(f"  {r['keyword_match_type']:<25} imps={r['kw_impressions']:>8.0f} ({r['kw_impressions']/total_imp*100:5.1f}%)  "
              f"clicks={r['kw_clicks']:>6.0f}  CTR={ctr:.4f}  CVR={cvr:.4f}")

# Keyword status distribution for problematic
print("\n--- Keyword status for PROBLEMATIC ad groups ---")
kwp = kw[kw['is_problematic']]
print(kwp.groupby('kw_status').agg(impressions=('kw_impressions','sum'), clicks=('kw_clicks','sum')).reset_index())

# Analyze keyword text patterns in problematic groups
print("\n--- Keyword text samples in problematic ad groups (top by impressions) ---")
kwp_text = kw18[kw18['ad_group_id'].isin(prob_ids)].sort_values('kw_impressions', ascending=False)
print(kwp_text.head(40).to_string())