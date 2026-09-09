import pandas as pd
import numpy as np
import json
import re
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Load all ad groups
cols_ag = ['ad_group_id', 'ad_group_name', 'campaign_id', 'campaign_name', 'account_name', 'status',
           'impressions', 'clicks', 'spend', 'conversions', 'conv_value', 'vtc', 'ctr', 'cvr']
ag = pd.DataFrame([json.loads(l) for l in open('/results/S16.rows.jsonl')], columns=cols_ag)

# Load campaign data for campaign_cvr
cols_cam = ['campaign_id', 'campaign_name', 'account_name', 'advertising_channel_type', 'advertising_channel_subtype', 'status',
            'campaign_impressions', 'campaign_clicks', 'campaign_spend', 'campaign_conversions', 'campaign_cvr']
cam = pd.DataFrame([json.loads(l) for l in open('/results/S17.rows.jsonl')], columns=cols_cam)
ag = ag.merge(cam[['campaign_id', 'campaign_cvr']], on='campaign_id', how='left')

ctr_p75 = np.percentile(ag['ctr'], 75)
cvr_p25 = np.percentile(ag['cvr'], 25)
ag['is_problematic'] = (ag['ctr'] > ctr_p75) & (ag['cvr'] < cvr_p25)

# Intent Match Ratio
ag['intent_match_ratio'] = np.where(ag['campaign_cvr'] > 0, ag['cvr'] / ag['campaign_cvr'], 0)

prob = ag[ag['is_problematic']]
nonprob = ag[~ag['is_problematic']]

# IMR distribution
print("--- Intent Match Ratio (problematic) ---")
p_imr = prob['intent_match_ratio']
print(f"Mean: {p_imr.mean():.4f}, Median: {p_imr.median():.4f}")
print(f"Std: {p_imr.std():.4f}")
print(f"% with IMR < 0.5: {(p_imr < 0.5).mean()*100:.1f}%")
print(f"% with IMR < 0.7: {(p_imr < 0.7).mean()*100:.1f}%")

nprob_imr = nonprob['intent_match_ratio']
print(f"\n--- Intent Match Ratio (non-problematic) ---")
print(f"Mean: {nprob_imr.mean():.4f}, Median: {nprob_imr.median():.4f}")
print(f"Std: {nprob_imr.std():.4f}")
print(f"% with IMR < 0.5: {(nprob_imr < 0.5).mean()*100:.1f}%")

# Traffic quality metrics
ag['cpc'] = ag['spend'] / ag['clicks'].replace(0, np.nan)
ag['cpm'] = ag['spend'] / ag['impressions'].replace(0, np.nan) * 1000
ag['cv_per_click'] = ag['conv_value'] / ag['clicks'].replace(0, np.nan)
ag['roas'] = ag['conv_value'] / ag['spend'].replace(0, np.nan)

print("\n--- Traffic quality: problematic vs non-problematic ---")
for metric in ['cpc', 'cpm', 'cv_per_click', 'roas', 'impressions', 'clicks', 'spend', 'conv_value']:
    p_mean = prob[metric].mean()
    p_med = prob[metric].median()
    np_mean = nonprob[metric].mean()
    np_med = nonprob[metric].median()
    print(f"  {metric:20s}: prob mean={p_mean:10.2f} median={p_med:8.2f} | nonprob mean={np_mean:10.2f} median={np_med:8.2f}")

# CTR vs CVR scatter plot
fig, ax = plt.subplots(figsize=(10, 6))
colors = ['red' if x else 'blue' for x in ag['is_problematic']]
ax.scatter(ag['ctr'], ag['cvr'], c=colors, alpha=0.3, s=15)
ax.axvline(x=ctr_p75, color='green', linestyle='--', label=f'CTR p75={ctr_p75:.4f}')
ax.axhline(y=cvr_p25, color='orange', linestyle='--', label=f'CVR p25={cvr_p25:.4f}')
ax.set_xlabel('CTR (Click-Through Rate)')
ax.set_ylabel('CVR (Conversion Rate)')
ax.set_title('CTR vs CVR by Ad Group\nRed = Problematic (High CTR, Low CVR)')
ax.legend()
ax.set_xlim(0, 0.12)
ax.set_ylim(0, 0.11)
plt.tight_layout()
plt.savefig('/work/ctr_cvr_scatter.png', dpi=100)
print("\nScatter plot saved.")

# IMR histogram
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.hist(prob['intent_match_ratio'].clip(0, 3), bins=30, alpha=0.7, color='red')
ax1.set_title('Problematic: Intent Match Ratio')
ax1.set_xlabel('IMR (Actual CVR / Expected CVR)')
ax1.axvline(x=1, color='black', linestyle='--', label='IMR=1')
ax1.legend()

ax2.hist(nonprob['intent_match_ratio'].clip(0, 3), bins=30, alpha=0.7, color='blue')
ax2.set_title('Non-Problematic: Intent Match Ratio')
ax2.set_xlabel('IMR (Actual CVR / Expected CVR)')
ax2.axvline(x=1, color='black', linestyle='--', label='IMR=1')
ax2.legend()
plt.tight_layout()
plt.savefig('/work/imr_histogram.png', dpi=100)
print("IMR histogram saved.")

# Campaign channel analysis with IMR
def parse_campaign(name):
    part = name.split(' - ')[0].strip()
    parts = part.split()
    channel = parts[0] if parts else ''
    strategy = ' '.join(parts[1:]) if len(parts) > 1 else ''
    return channel, strategy

ag[['campaign_channel', 'campaign_strategy']] = ag['campaign_name'].apply(lambda n: pd.Series(parse_campaign(n)))

print("\n--- IMR by campaign channel (problematic only) ---")
for ch in ['Search', 'Brand', 'Display', 'Shopping', 'Performance']:
    sub = prob[prob['campaign_channel'] == ch]
    if len(sub) > 0:
        print(f"  {ch:15s}: n={len(sub):3d}, mean IMR={sub['intent_match_ratio'].mean():.4f}")

print("\n--- IMR by campaign strategy (problematic only) ---")
for st in ['Broad', 'Exact', 'Keywords', 'Remarketing', 'Audience']:
    sub = prob[prob['campaign_strategy'] == st]
    if len(sub) > 0:
        print(f"  {st:15s}: n={len(sub):3d}, mean IMR={sub['intent_match_ratio'].mean():.4f}")

# Save final analysis
ag.to_csv('/work/ag_full_analysis.csv', index=False)