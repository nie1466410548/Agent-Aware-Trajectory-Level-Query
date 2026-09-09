import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

def load_rows(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

cols71 = ["campaign_id","campaign_name","account_id","account_name","days_running","camp_last_date","date_day",
          "campaign_lifecycle_stage","advertising_channel_type","advertising_channel_subtype","customer_maturity_stage",
          "account_maturity_stage","strategic_customer_segment","customer_acquisition_cost","ltv_cac_ratio","spend",
          "conversions","conversions_value","acquisition_sophistication_score","cac_efficiency_percentile",
          "channel_diversity_count","retention_risk","scale_opportunity","high_cac_alert","negative_roi_alert",
          "cac_performance_tier","acquisition_efficiency_tier","acquisition_recommendation","roas","cpc","ctr",
          "estimated_payback_days","active_campaigns_count","cumulative_acquisition_cost","cumulative_conversions",
          "cumulative_ltv","cac_vs_cohort_pct","ltv_vs_cohort_pct","jd"]
df = pd.DataFrame(load_rows('/results/S71.rows.jsonl'), columns=cols71)

# Decayed zones
decay_zones = [
    ('ACC_FIN_001','SHOPPING','SHOPPING_GOAL_OPTIMIZED_ADS'),
    ('ACC_ECOM_002','VIDEO','YOUTUBE_SEARCH')
]

df['is_decay_zone'] = df.apply(lambda r: (r['account_id'], r['advertising_channel_type'], r['advertising_channel_subtype']) in decay_zones, axis=1)

# Convert date
df['date_dt'] = pd.to_datetime(df['date_day'].str[:10])

# Focus on the decayed zones
print("=== DECAYED ZONES: DIMENSION PROFILES ===")
dz = df[df['is_decay_zone']]
print(f"Total rows in decay zones: {len(dz)}")

# By lifecycle stage within decay zones
print("\n--- Lifecycle stage profile in decay zones ---")
prof = dz.groupby('campaign_lifecycle_stage').agg(
    n=('campaign_id','count'),
    avg_cac=('customer_acquisition_cost','mean'),
    avg_ltv_cac=('ltv_cac_ratio','mean'),
    avg_soph=('acquisition_sophistication_score','mean'),
    avg_eff=('cac_efficiency_percentile','mean'),
    ret_risk=('retention_risk','mean'),
    scale_opp=('scale_opportunity','mean'),
    high_cac=('high_cac_alert','mean')
).reset_index()
print(prof.to_string(index=False))

# By customer maturity stage
print("\n--- Customer maturity profile in decay zones ---")
prof2 = dz.groupby('customer_maturity_stage').agg(
    n=('campaign_id','count'),
    avg_cac=('customer_acquisition_cost','mean'),
    avg_ltv_cac=('ltv_cac_ratio','mean'),
    avg_soph=('acquisition_sophistication_score','mean'),
    ret_risk=('retention_risk','mean')
).reset_index()
print(prof2.to_string(index=False))

# By strategic customer segment
print("\n--- Strategic customer segment profile in decay zones ---")
prof3 = dz.groupby('strategic_customer_segment').agg(
    n=('campaign_id','count'),
    avg_cac=('customer_acquisition_cost','mean'),
    avg_ltv_cac=('ltv_cac_ratio','mean'),
    avg_soph=('acquisition_sophistication_score','mean'),
    avg_eff=('cac_efficiency_percentile','mean'),
    ret_risk=('retention_risk','mean'),
    scale_opp=('scale_opportunity','mean'),
    high_cac=('high_cac_alert','mean'),
    neg_roi=('negative_roi_alert','mean'),
    avg_chdiv=('channel_diversity_count','mean'),
    avg_payback=('estimated_payback_days','mean')
).reset_index()
print(prof3.to_string(index=False))

# By account maturity
print("\n--- Account maturity profile in decay zones ---")
prof4 = dz.groupby('account_maturity_stage').agg(
    n=('campaign_id','count'),
    avg_cac=('customer_acquisition_cost','mean'),
    avg_ltv_cac=('ltv_cac_ratio','mean'),
    avg_soph=('acquisition_sophistication_score','mean')
).reset_index()
print(prof4.to_string(index=False))

# Channel saturation & competitive intensity proxies
print("\n\n=== CHANNEL SATURATION & COMPETITIVE INTENSITY PROXIES ===")
dz_stats = dz.groupby(['account_id','advertising_channel_type']).agg(
    n=('campaign_id','count'),
    avg_active_campaigns=('active_campaigns_count','mean'),
    avg_channel_diversity=('channel_diversity_count','mean'),
    avg_cac_vs_cohort=('cac_vs_cohort_pct','mean'),
    avg_ltv_vs_cohort=('ltv_vs_cohort_pct','mean'),
    high_cac_rate=('high_cac_alert','mean'),
    neg_roi_rate=('negative_roi_alert','mean'),
    avg_cac=('customer_acquisition_cost','mean'),
    avg_ltv_cac=('ltv_cac_ratio','mean')
).reset_index()
print(dz_stats.to_string(index=False))

# Compare decay zones vs healthy zones (same channels elsewhere)
print("\n\n=== DECAY ZONES vs OTHER ZONES (same channel) ===")
for ch in ['SHOPPING','VIDEO']:
    print(f"\n--- {ch} channel ---")
    ch_df = df[(df['advertising_channel_type']==ch) & (df['account_id']!='ACC_HLTH_001')]
    for acct in ch_df['account_id'].unique():
        sub = ch_df[ch_df['account_id']==acct]
        is_decay = (acct, ch, sub['advertising_channel_subtype'].iloc[0]) in decay_zones
        print(f"  {acct} ({sub['advertising_channel_subtype'].iloc[0]}): {'DECAY' if is_decay else 'ok'} | "
              f"n={len(sub)}, Avg CAC={sub['customer_acquisition_cost'].mean():.1f}, "
              f"Avg LTV/CAC={sub['ltv_cac_ratio'].mean():.1f}, "
              f"Avg Soph={sub['acquisition_sophistication_score'].mean():.1f}, "
              f"RetRisk={sub['retention_risk'].mean()*100:.1f}%")

# ===== BUDGET REALLOCATION MODEL =====
print("\n\n=== BUDGET REALLOCATION RECOMMENDATION MODEL ===")

# Compute spend-weighted efficiency metrics per strategic segment in decay zones
# For each segment: acquisition efficiency = LTV/CAC, scale opportunity, spend
seg_efficiency = dz.groupby('strategic_customer_segment').agg(
    spend=('spend','sum'),
    conv=('conversions','sum'),
    ltv_cac=('ltv_cac_ratio','mean'),
    cac=('customer_acquisition_cost','mean'),
    scale_opp=('scale_opportunity','mean'),
    ret_risk=('retention_risk','mean'),
    soph=('acquisition_sophistication_score','mean')
).reset_index()
seg_efficiency['spend_share'] = seg_efficiency['spend'] / seg_efficiency['spend'].sum()
seg_efficiency['efficiency_index'] = seg_efficiency['ltv_cac'] / seg_efficiency['cac'].replace(0, np.nan)
seg_efficiency['recommendation_priority'] = seg_efficiency['efficiency_index'] * (1 - seg_efficiency['ret_risk']) * (0.5 + seg_efficiency['scale_opp'])
print("Segment efficiency in decay zones:")
print(seg_efficiency.sort_values('recommendation_priority', ascending=False).to_string(index=False))

# Overall recommendation summary
print("\n\n=== KEY RECOMMENDATIONS BY SEGMENT ===")
print("HIGH-VALUE (protect/invest): Enterprise, High Value B2B, VIP customers - high LTV/CAC")
print("HIGH-RISK (reduce/optimize): Bargain Hunters, Consumer Standard - low LTV/CAC, high retention risk")
print("CHANNEL: SHOPPING (SmartInvest) shows worst CAC inflation (+67.7%)")
print("CHANNEL: VIDEO/YOUTUBE_SEARCH (FashionForward) shows efficiency decay (CAC +37.3%)")

# Save a summary plot of segment efficiency in decay zones
plt.figure(figsize=(12, 6))
seg_plot = seg_efficiency.sort_values('efficiency_index', ascending=False)
plt.bar(seg_plot['strategic_customer_segment'], seg_plot['efficiency_index'], color='#2166ac', alpha=0.8)
plt.ylabel('Efficiency Index (LTV/CAC per unit CAC)')
plt.title('Acquisition Efficiency by Strategic Segment in Decayed Campaign Zones')
plt.xticks(rotation=45, ha='right')
for i, v in enumerate(seg_plot['efficiency_index']):
    plt.text(i, v, f'{v:.2f}', ha='center', va='bottom', fontsize=9)
plt.tight_layout()
plt.savefig('/work/segment_efficiency_decay_zones.png', dpi=150)
plt.close()
print("Saved: segment_efficiency_decay_zones.png")