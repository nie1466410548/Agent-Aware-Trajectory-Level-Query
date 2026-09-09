import pandas as pd
import numpy as np
import json, re

# Load data for final comprehensive stats
cols_ag = ['ad_group_id', 'ad_group_name', 'campaign_id', 'campaign_name', 'account_name', 'status',
           'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S16.rows.jsonl')], columns=cols_ag)

cols_cam = ['campaign_id', 'campaign_name', 'account_name', 'advertising_channel_type', 'advertising_channel_subtype', 'status',
            'campaign_impressions', 'campaign_clicks', 'campaign_spend', 'campaign_conversions', 'campaign_cvr']
cam = pd.DataFrame([json.loads(l) for l in open('/results/S17.rows.jsonl')], columns=cols_cam)

ag = ag.merge(cam[['campaign_id', 'campaign_cvr']], on='campaign_id', how='left')

ctr_p75 = np.percentile(ag['ctr'], 75)
cvr_p25 = np.percentile(ag['cvr'], 25)
ag['is_problematic'] = (ag['ctr'] > ctr_p75) & (ag['cvr'] < cvr_p25)
ag['intent_match_ratio'] = np.where(ag['campaign_cvr'] > 0, ag['cvr'] / ag['campaign_cvr'], 0)

prob = ag[ag['is_problematic']]
nonprob = ag[~ag['is_problematic']]

# Calculate total spend wasted
total_spend_prob = prob['spend'].sum()
total_spend_all = ag['spend'].sum()
total_conv_prob = prob['conversions'].sum()
total_conv_all = ag['conversions'].sum()

print(f"Total spend on problematic: ${total_spend_prob:.2f} ({total_spend_prob/total_spend_all*100:.1f}% of total)")
print(f"Total conversions from problematic: {total_conv_prob:.1f} ({total_conv_prob/total_conv_all*100:.1f}% of total)")
print(f"Problematic spend/conv ratio: {total_spend_prob/total_conv_prob:.2f} vs overall: {total_spend_all/total_conv_all:.2f}")

# By campaign channel using campaign_report data
ag_chan = ag.merge(cam[['campaign_id', 'advertising_channel_type', 'advertising_channel_subtype']], on='campaign_id', how='left')

print("\n--- Problematic conversion rate by channel ---")
prob_chan = prob.merge(cam[['campaign_id', 'advertising_channel_type', 'advertising_channel_subtype']], on='campaign_id', how='left')
for ch in prob_chan['advertising_channel_type'].unique():
    sub = prob_chan[prob_chan['advertising_channel_type'] == ch]
    print(f"  {ch:15s}: n={len(sub):3d}, mean CVR={sub['cvr'].mean():.4f}, mean IMR={sub['intent_match_ratio'].mean():.4f}")

# Average CTR and CVR thresholds
print(f"\n--- Thresholds ---")
print(f"CTR p75: {ctr_p75:.6f}")
print(f"CVR p25: {cvr_p25:.6f}")
print(f"Problematic CTR range: {prob['ctr'].min():.6f} - {prob['ctr'].max():.6f}")
print(f"Problematic CVR range: {prob['cvr'].min():.6f} - {prob['cvr'].max():.6f}")

# Check ad group name patterns
print(f"\nUnique ad group names in problematic: {prob['ad_group_name'].nunique()}")
print(f"Unique ad group names in non-problematic: {nonprob['ad_group_name'].nunique()}")
# They all seem to be the same encoded name "G+b561Y/O/hceLQhm/Cd6Q=="
print(f"Sample ad group names: {prob['ad_group_name'].unique()[:3]}")

# Count of ad groups with zero conversions
zero_conv_prob = (prob['conversions'] == 0).sum()
zero_conv_nonprob = (nonprob['conversions'] == 0).sum()
print(f"\nZero conversion ad groups: problem={zero_conv_prob} ({zero_conv_prob/len(prob)*100:.1f}%), non-problem={zero_conv_nonprob} ({zero_conv_nonprob/len(nonprob)*100:.1f}%)")

# Cost per conversion for problematic groups
prob['cpa'] = prob['spend'] / prob['conversions'].replace(0, np.nan)
nonprob['cpa'] = nonprob['spend'] / nonprob['conversions'].replace(0, np.nan)
print(f"CPA (excluding zero conv): problem mean=${prob[prob['conversions']>0]['cpa'].mean():.2f}, non-problem mean=${nonprob[nonprob['conversions']>0]['cpa'].mean():.2f}")