import pandas as pd
import numpy as np
import json

# Load ad group data with campaign_id
cols_ag = ['ad_group_id', 'ad_group_name', 'campaign_id', 'campaign_name', 'account_name', 'status',
           'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S16.rows.jsonl')], columns=cols_ag)

# Load campaign data
cols_cam = ['campaign_id', 'campaign_name', 'account_name', 'advertising_channel_type', 'advertising_channel_subtype', 'status',
            'campaign_impressions', 'campaign_clicks', 'campaign_spend', 'campaign_conversions', 'campaign_cvr']
cam = pd.DataFrame([json.loads(l) for l in open('/results/S17.rows.jsonl')], columns=cols_cam)

# Merge with campaign data
ag = ag.merge(cam[['campaign_id', 'advertising_channel_type', 'advertising_channel_subtype', 'campaign_cvr']], on='campaign_id', how='left')

# Compute percentiles
ctr_p75 = np.percentile(ag['ctr'], 75)
cvr_p25 = np.percentile(ag['cvr'], 25)
print(f"CTR p75: {ctr_p75:.6f}")
print(f"CVR p25: {cvr_p25:.6f}")

# Flag problematic
ag['is_problematic'] = (ag['ctr'] > ctr_p75) & (ag['cvr'] < cvr_p25)
problematic = ag[ag['is_problematic']].copy()
non_problematic = ag[~ag['is_problematic']].copy()

print(f"Problematic: {len(problematic)} / {len(ag)} ({len(problematic)/len(ag)*100:.2f}%)")

# Compute Intent Match Ratio = actual CVR / expected CVR (campaign-level CVR)
# For ad groups where campaign_cvr is 0, handle gracefully
problematic['intent_match_ratio'] = np.where(problematic['campaign_cvr'] > 0, 
                                             problematic['cvr'] / problematic['campaign_cvr'], 0)
non_problematic['intent_match_ratio'] = np.where(non_problematic['campaign_cvr'] > 0,
                                                 non_problematic['cvr'] / non_problematic['campaign_cvr'], 0)

print("\n--- Intent Match Ratio comparison ---")
print(f"Problematic - mean IMR: {problematic['intent_match_ratio'].mean():.4f}, median: {problematic['intent_match_ratio'].median():.4f}")
print(f"Non-problematic - mean IMR: {non_problematic['intent_match_ratio'].mean():.4f}, median: {non_problematic['intent_match_ratio'].median():.4f}")

# Channel type distribution
print("\n--- Channel type distribution (problematic vs non-problematic) ---")
prob_chan = problematic['advertising_channel_type'].value_counts()
nonprob_chan = non_problematic['advertising_channel_type'].value_counts()
chan_compare = pd.DataFrame({
    'Problematic': prob_chan,
    'Non-Problematic': nonprob_chan,
    'Prob%': (prob_chan / len(problematic) * 100).round(1),
    'NonProb%': (nonprob_chan / len(non_problematic) * 100).round(1)
}).fillna(0)
print(chan_compare)

# Channel subtype distribution
print("\n--- Channel subtype distribution ---")
prob_sub = problematic['advertising_channel_subtype'].value_counts()
nonprob_sub = non_problematic['advertising_channel_subtype'].value_counts()
sub_compare = pd.DataFrame({
    'Problematic': prob_sub,
    'Non-Problematic': nonprob_sub,
    'Prob%': (prob_sub / len(problematic) * 100).round(1),
    'NonProb%': (nonprob_sub / len(non_problematic) * 100).round(1)
}).fillna(0)
print(sub_compare)

# Status distribution
print("\n--- Status distribution ---")
print("Problematic status:")
print(problematic['status'].value_counts())
print("\nNon-problematic status:")
print(non_problematic['status'].value_counts())

# CPA (cost per acquisition) comparison
problematic['cpa'] = problematic['spend'] / problematic['conversions'].replace(0, np.nan)
non_problematic['cpa'] = non_problematic['spend'] / non_problematic['conversions'].replace(0, np.nan)
print(f"\n--- CPA comparison ---")
print(f"Problematic - mean CPA: ${problematic['cpa'].mean():.2f}, median: ${problematic['cpa'].median():.2f}")
print(f"Non-problematic - mean CPA: ${non_problematic['cpa'].mean():.2f}, median: ${non_problematic['cpa'].median():.2f}")

# Summary stats for problematic groups
print("\n--- Problematic ad groups summary stats ---")
print(problematic[['ctr', 'cvr', 'intent_match_ratio', 'impressions', 'clicks', 'conversions', 'spend']].describe())

# Save problematic data for later analysis
problematic.to_csv('/work/problematic_analysis.csv', index=False)
ag.to_csv('/work/all_adgroups.csv', index=False)