import pandas as pd
import numpy as np
import json

# Load the full analysis
ag = pd.read_csv('/work/ag_full_analysis.csv')

prob = ag[ag['is_problematic']]
nonprob = ag[~ag['is_problematic']]

# Account-level analysis
print("--- Account distribution (problematic) ---")
acc_prob = prob['account_name'].value_counts()
acc_nonprob = nonprob['account_name'].value_counts()
acc_compare = pd.DataFrame({
    'Problematic': acc_prob,
    'Non-Problematic': acc_nonprob,
    'Prob%': (acc_prob / len(prob) * 100).round(1),
    'NonProb%': (acc_nonprob / len(nonprob) * 100).round(1)
}).fillna(0)
print(acc_compare.head(20).to_string())

# Check if some accounts have higher problem rates
prob_rate_by_account = ag.groupby('account_name')['is_problematic'].mean() * 100
print("\n--- Accounts with highest problem rate ---")
print(prob_rate_by_account.sort_values(ascending=False).head(15).to_string())

# Campaign type distribution from campaign_report
cols_cam = ['campaign_id', 'campaign_name', 'account_name', 'advertising_channel_type', 'advertising_channel_subtype', 'status',
            'campaign_impressions', 'campaign_clicks', 'campaign_spend', 'campaign_conversions', 'campaign_cvr']
cam = pd.DataFrame([json.loads(l) for l in open('/results/S17.rows.jsonl')], columns=cols_cam)

# Check if advertising_channel_type from campaign report matches campaign name channel
ag_with_chan = ag.merge(cam[['campaign_id', 'advertising_channel_type', 'advertising_channel_subtype']], on='campaign_id', how='left')
print("\n--- Advertising channel type vs problematic ---")
chan_type = ag_with_chan.groupby(['advertising_channel_type', 'is_problematic']).size().unstack(fill_value=0)
chan_type['prob_rate'] = chan_type[True] / (chan_type[True] + chan_type[False]) * 100
print(chan_type.sort_values('prob_rate', ascending=False).to_string())

# Advertising channel subtype vs problematic
print("\n--- Advertising channel subtype vs problematic ---")
sub_type = ag_with_chan.groupby(['advertising_channel_subtype', 'is_problematic']).size().unstack(fill_value=0)
sub_type['prob_rate'] = sub_type[True] / (sub_type[True] + sub_type[False]) * 100
print(sub_type.sort_values('prob_rate', ascending=False).to_string())

# Check aggregated keyword-level data for problematic groups
# Focus on keyword text patterns like "free", "discount", "cheap" - low intent keywords
cols_kw18 = ['ad_group_id', 'keyword_text', 'keyword_match_type', 'type', 'kw_status', 'kw_impressions', 'kw_clicks', 'kw_spend', 'kw_conversions']
kw18 = pd.DataFrame([json.loads(l) for l in open('/results/S18.rows.jsonl')], columns=cols_kw18)

# Identify low-intent keywords
low_intent_words = ['free', 'cheap', 'discount', 'buy', 'price', 'sale', 'warranty', 'support', 'review', 'delivery', 'price', 'deal', 'bargain', 'coupon']
def contains_low_intent(text):
    text_lower = text.lower()
    return any(word in text_lower for word in low_intent_words)

kw18['low_intent'] = kw18['keyword_text'].apply(contains_low_intent if hasattr(kw18['keyword_text'], 'apply') else lambda x: False)

# Actually check
kw18_low = kw18[kw18['keyword_text'].str.lower().apply(lambda t: any(w in t for w in low_intent_words))]
print(f"\n--- Low-intent keywords in problematic groups ---")
print(f"Total keywords: {len(kw18)}")
print(f"Low-intent keywords: {len(kw18_low)} ({len(kw18_low)/len(kw18)*100:.1f}%)")
print(f"Low-intent impressions: {kw18_low['kw_impressions'].sum():.0f} / {kw18['kw_impressions'].sum():.0f} ({kw18_low['kw_impressions'].sum()/kw18['kw_impressions'].sum()*100:.1f}%)")

# Top low-intent keywords
print("\nTop low-intent keywords by impressions:")
print(kw18_low.groupby('keyword_text').agg(imps=('kw_impressions','sum'), clks=('kw_clicks','sum'), conv=('kw_conversions','sum')).sort_values('imps', ascending=False).head(20).to_string())

# Calculate CTR and CVR for problematic ad groups at keyword level
kw_agg_prob = kw18.groupby('ad_group_id').agg(
    kw_imps=('kw_impressions', 'sum'), kw_clks=('kw_clicks', 'sum'), kw_conv=('kw_conversions', 'sum')
).reset_index()
kw_agg_prob['kw_ctr'] = kw_agg_prob['kw_clks'] / kw_agg_prob['kw_imps']
kw_agg_prob['kw_cvr'] = kw_agg_prob['kw_conv'] / kw_agg_prob['kw_clks'].replace(0, np.nan)
print(f"\nAggregated keyword-level CTR for problematic: {kw_agg_prob['kw_ctr'].mean():.4f}")
print(f"Aggregated keyword-level CVR for problematic: {kw_agg_prob['kw_cvr'].mean():.4f}")