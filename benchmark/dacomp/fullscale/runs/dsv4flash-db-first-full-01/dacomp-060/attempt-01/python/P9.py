import pandas as pd
import numpy as np
import json
import re

# Load all ad groups
cols_ag = ['ad_group_id', 'ad_group_name', 'campaign_id', 'campaign_name', 'account_name', 'status',
           'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S16.rows.jsonl')], columns=cols_ag)

ctr_p75 = np.percentile(ag['ctr'], 75)
cvr_p25 = np.percentile(ag['cvr'], 25)
ag['is_problematic'] = (ag['ctr'] > ctr_p75) & (ag['cvr'] < cvr_p25)

# Parse campaign name: "Channel Strategy - Season Year"
def parse_campaign(name):
    part = name.split(' - ')[0].strip()
    parts = part.split()
    channel = parts[0] if parts else ''
    strategy = ' '.join(parts[1:]) if len(parts) > 1 else ''
    return channel, strategy

ag[['campaign_channel', 'campaign_strategy']] = ag['campaign_name'].apply(lambda n: pd.Series(parse_campaign(n)))

print("--- Campaign channel vs problematic ---")
chan_prob = ag.groupby(['campaign_channel', 'is_problematic']).size().unstack(fill_value=0)
chan_prob['prob_rate'] = chan_prob[True] / (chan_prob[True] + chan_prob[False]) * 100
print(chan_prob.sort_values('prob_rate', ascending=False).to_string())

print("\n--- Campaign strategy vs problematic ---")
strat_prob = ag.groupby(['campaign_strategy', 'is_problematic']).size().unstack(fill_value=0)
strat_prob['prob_rate'] = strat_prob[True] / (strat_prob[True] + strat_prob[False]) * 100
print(strat_prob.sort_values('prob_rate', ascending=False).to_string())

# Traffic quality: cost per click, spend per impression
ag['cpc'] = ag['spend'] / ag['clicks'].replace(0, np.nan)
ag['cpm'] = ag['spend'] / ag['impressions'].replace(0, np.nan) * 1000
ag['conv_rate_per_impression'] = ag['conversions'] / ag['impressions'].replace(0, np.nan)

print("\n--- Traffic quality metrics comparison ---")
prob = ag[ag['is_problematic']]
nonprob = ag[~ag['is_problematic']]
for metric in ['cpc', 'cpm', 'impressions', 'clicks', 'spend', 'conv_value']:
    print(f"{metric}: problematic mean={prob[metric].mean():.2f} median={prob[metric].median():.2f} | "
          f"non-problematic mean={nonprob[metric].mean():.2f} median={nonprob[metric].median():.2f}")

# Conversion value per click / per conversion
prob['cv_per_click'] = prob['conv_value'] / prob['clicks'].replace(0, np.nan)
nonprob['cv_per_click'] = nonprob['conv_value'] / nonprob['clicks'].replace(0, np.nan)
prob['cv_per_conv'] = prob['conv_value'] / prob['conversions'].replace(0, np.nan)
nonprob['cv_per_conv'] = nonprob['conv_value'] / nonprob['conversions'].replace(0, np.nan)
print(f"\ncv_per_click: problematic mean={prob['cv_per_click'].mean():.2f} | non-problematic mean={nonprob['cv_per_click'].mean():.2f}")
print(f"cv_per_conv: problematic mean={prob['cv_per_conv'].mean():.2f} | non-problematic mean={nonprob['cv_per_conv'].mean():.2f}")

# ROAS
prob['roas'] = prob['conv_value'] / prob['spend'].replace(0, np.nan)
nonprob['roas'] = nonprob['conv_value'] / nonprob['spend'].replace(0, np.nan)
print(f"ROAS: problematic mean={prob['roas'].mean():.2f} median={prob['roas'].median():.2f} | non-problematic mean={nonprob['roas'].mean():.2f} median={nonprob['roas'].median():.2f}")

# Save parsed data
ag.to_csv('/work/ag_with_campaign.csv', index=False)

# Intent match ratio - distribution
ag['intent_match_ratio'] = np.where(ag['campaign_cvr'] > 0, ag['cvr'] / ag['campaign_cvr'], 0)
# Actually need campaign_cvr - load campaign data
cols_cam = ['campaign_id', 'campaign_name', 'account_name', 'advertising_channel_type', 'advertising_channel_subtype', 'status',
            'campaign_impressions', 'campaign_clicks', 'campaign_spend', 'campaign_conversions', 'campaign_cvr']
cam = pd.DataFrame([json.loads(l) for l in open('/results/S17.rows.jsonl')], columns=cols_cam)
ag = ag.merge(cam[['campaign_id', 'campaign_cvr']], on='campaign_id', how='left')
ag['intent_match_ratio'] = np.where(ag['campaign_cvr'] > 0, ag['cvr'] / ag['campaign_cvr'], 0)

# IMR distribution of problematic
p_imr = ag[ag['is_problematic']]['intent_match_ratio']
print(f"\n--- Intent Match Ratio distribution (problematic) ---")
print(p_imr.describe())
print(f"% with IMR < 0.5: {(p_imr < 0.5).mean()*100:.1f}%")
print(f"% with IMR < 0.7: {(p_imr < 0.7).mean()*100:.1f}%")