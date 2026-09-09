import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Read the joined dataset (S71) and campaign-level metrics (S72)
df_joined = pd.read_json('/results/S71.rows.jsonl', lines=True)
df_camp_metrics = pd.read_json('/results/S72.rows.jsonl', lines=True)

print(f"Joined rows: {len(df_joined)}")
print(f"Campaign metrics rows: {len(df_camp_metrics)}")
print(f"Columns: {df_joined.columns.tolist()}")

# Compute campaign-level metrics
# CAC = spend/conversions (weighted)
# LTV/CAC = conversions-weighted average
df_camp_metrics['cac_last'] = df_camp_metrics['spend_last'] / df_camp_metrics['conv_last'].replace(0, np.nan)
df_camp_metrics['cac_prior'] = df_camp_metrics['spend_prior'] / df_camp_metrics['conv_prior'].replace(0, np.nan)
df_camp_metrics['ltv_cac_last'] = df_camp_metrics['ltv_cac_w_last'] / df_camp_metrics['conv_last'].replace(0, np.nan)
df_camp_metrics['ltv_cac_prior'] = df_camp_metrics['ltv_cac_w_prior'] / df_camp_metrics['conv_prior'].replace(0, np.nan)

df_camp_metrics['cac_growth'] = (df_camp_metrics['cac_last'] - df_camp_metrics['cac_prior']) / df_camp_metrics['cac_prior'].replace(0, np.nan)
df_camp_metrics['ltv_cac_change'] = (df_camp_metrics['ltv_cac_last'] - df_camp_metrics['ltv_cac_prior']) / df_camp_metrics['ltv_cac_prior'].replace(0, np.nan)

df_camp_metrics['decay_flag'] = ((df_camp_metrics['cac_growth'] > 0.25) & (df_camp_metrics['ltv_cac_change'] < -0.20)).astype(int)

print(f"\n=== CAMPAIGN DECAY ANALYSIS ===")
print(f"Total campaigns with sufficient data: {len(df_camp_metrics)}")
print(f"Campaigns with CAC growth >25% and LTV/CAC decline >20%: {df_camp_metrics['decay_flag'].sum()}")

decay_camps = df_camp_metrics[df_camp_metrics['decay_flag'] == 1]
print(f"\nDecayed campaigns:")
for _, row in decay_camps.iterrows():
    print(f"  {row['campaign_id']} ({row['account_name']}) - {row['advertising_channel_type']}/{row['advertising_channel_subtype']}")
    print(f"    CAC: {row['cac_prior']:.2f} -> {row['cac_last']:.2f} (growth: {row['cac_growth']*100:.1f}%)")
    print(f"    LTV/CAC: {row['ltv_cac_prior']:.2f} -> {row['ltv_cac_last']:.2f} (change: {row['ltv_cac_change']*100:.1f}%)")

# ===== MULTI-DIMENSIONAL ANALYSIS =====
print(f"\n\n=== MULTI-DIMENSIONAL ANALYSIS ===")

# Analyze by campaign_lifecycle_stage
# Map the joined data to compute decay risk per segment
# First, let's compute per-campaign-lifecycle-stage metrics
df_joined['jd'] = pd.to_numeric(df_joined['jd'])  # julianday
df_joined['camp_last_date'] = pd.to_datetime(df_joined['camp_last_date'])
df_joined['date_day_dt'] = pd.to_datetime(df_joined['date_day'].str[:10])

# For each campaign, calculate window membership
# We need ref_jd, which is julianday of camp_last_date
from datetime import datetime, timedelta

# Compute ref_jd for each campaign
camp_refs = df_joined.groupby('campaign_id')['camp_last_date'].first().reset_index()
camp_refs['ref_jd'] = camp_refs['camp_last_date'].apply(lambda x: (pd.Timestamp(x) - pd.Timestamp('2000-01-01')).days + 2451545)

# Actually, let me use a simpler approach: compute per-segment metrics directly
# Let me look at the segment-level decay patterns

# Get the flagged campaigns' account+channel combinations
decay_keys = decay_camps[['account_id', 'advertising_channel_type', 'advertising_channel_subtype']].drop_duplicates()
print(f"\nDistinct decay zones (account+channel): {len(decay_keys)}")
for _, r in decay_keys.iterrows():
    print(f"  {r['account_id']} | {r['advertising_channel_type']} | {r['advertising_channel_subtype']}")

# ===== DECAY RISK MODEL =====
print(f"\n\n=== DECAY RISK ASSESSMENT MODEL ===")

# Build a risk score for each campaign based on multiple factors
# Factors: cac_growth (positive), ltv_cac_change (negative), 
# acquisition_sophistication_score (lower = higher risk),
# cac_efficiency_percentile (lower = higher risk),
# channel_diversity_count (lower = higher risk),
# retention_risk (higher = higher risk),
# high_cac_alert, negative_roi_alert

# Normalize factors and compute composite risk score
df_camp_metrics['risk_factors'] = 0.0

# CAC growth risk (0-1): higher growth = higher risk
max_cac_growth = df_camp_metrics['cac_growth'].max()
df_camp_metrics['cac_growth_risk'] = df_camp_metrics['cac_growth'].clip(0) / max_cac_growth if max_cac_growth > 0 else 0

# LTV/CAC decline risk (0-1): more negative change = higher risk
min_ltv_change = df_camp_metrics['ltv_cac_change'].min()
df_camp_metrics['ltv_decline_risk'] = (-df_camp_metrics['ltv_cac_change'].clip(upper=0)) / (-min_ltv_change) if min_ltv_change < 0 else 0

# Sophistication risk (inverted): lower score = higher risk
max_soph = df_camp_metrics['soph_score_last'].max()
min_soph = df_camp_metrics['soph_score_last'].min()
df_camp_metrics['soph_risk'] = 1 - (df_camp_metrics['soph_score_last'] - min_soph) / (max_soph - min_soph) if max_soph > min_soph else 0

# Efficiency risk (inverted): lower percentile = higher risk
max_eff = df_camp_metrics['eff_perc_last'].max()
min_eff = df_camp_metrics['eff_perc_last'].min()
df_camp_metrics['eff_risk'] = 1 - (df_camp_metrics['eff_perc_last'] - min_eff) / (max_eff - min_eff) if max_eff > min_eff else 0

# Channel diversity risk (inverted): lower diversity = higher risk
max_ch = df_camp_metrics['ch_div_last'].max()
min_ch = df_camp_metrics['ch_div_last'].min()
df_camp_metrics['ch_div_risk'] = 1 - (df_camp_metrics['ch_div_last'] - min_ch) / (max_ch - min_ch) if max_ch > min_ch else 0

# Retention risk alert
df_camp_metrics['retention_risk_norm'] = df_camp_metrics['retention_risk_last'] / df_camp_metrics['retention_risk_last'].max() if df_camp_metrics['retention_risk_last'].max() > 0 else 0

# Composite risk score (weighted)
weights = {'cac_growth': 0.25, 'ltv_decline': 0.25, 'soph': 0.15, 'eff': 0.15, 'ch_div': 0.10, 'retention': 0.10}
df_camp_metrics['risk_score'] = (
    weights['cac_growth'] * df_camp_metrics['cac_growth_risk'] +
    weights['ltv_decline'] * df_camp_metrics['ltv_decline_risk'] +
    weights['soph'] * df_camp_metrics['soph_risk'] +
    weights['eff'] * df_camp_metrics['eff_risk'] +
    weights['ch_div'] * df_camp_metrics['ch_div_risk'] +
    weights['retention'] * df_camp_metrics['retention_risk_norm']
)

# Classify risk tiers
df_camp_metrics['risk_tier'] = pd.cut(df_camp_metrics['risk_score'], 
                                      bins=[0, 0.25, 0.5, 0.75, 1.0],
                                      labels=['Low', 'Medium', 'High', 'Critical'])

print(f"\nRisk distribution:")
print(df_camp_metrics['risk_tier'].value_counts().sort_index())

print(f"\nHigh/Critical risk campaigns:")
for _, row in df_camp_metrics[df_camp_metrics['risk_tier'].isin(['High', 'Critical'])].sort_values('risk_score', ascending=False).iterrows():
    print(f"  {row['campaign_id']} ({row['account_name']}) - {row['advertising_channel_type']}")
    print(f"    Risk Score: {row['risk_score']:.3f}, Tier: {row['risk_tier']}")
    print(f"    CAC Growth: {row['cac_growth']*100:.1f}%, LTV/CAC Change: {row['ltv_cac_change']*100:.1f}%")
    print(f"    Soph Score: {row['soph_score_last']}, Eff Perc: {row['eff_perc_last']}, Ch Div: {row['ch_div_last']}")

# ===== SEGMENT-LEVEL ANALYSIS =====
print(f"\n\n=== SEGMENT-LEVEL DECAY PATTERNS ===")

# Analyze by campaign_lifecycle_stage
lifecycle_analysis = df_joined.groupby('campaign_lifecycle_stage').agg(
    avg_cac=('customer_acquisition_cost', 'mean'),
    avg_ltv_cac=('ltv_cac_ratio', 'mean'),
    avg_soph=('acquisition_sophistication_score', 'mean'),
    avg_eff=('cac_efficiency_percentile', 'mean'),
    avg_chdiv=('channel_diversity_count', 'mean'),
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
    high_cac_rate=('high_cac_alert', 'mean'),
    neg_roi_rate=('negative_roi_alert', 'mean'),
    n_rows=('campaign_id', 'count')
).reset_index()

print(f"\nBy Campaign Lifecycle Stage:")
print(lifecycle_analysis.to_string(index=False))

# Analyze by advertising_channel_type
channel_analysis = df_joined.groupby('advertising_channel_type').agg(
    avg_cac=('customer_acquisition_cost', 'mean'),
    avg_ltv_cac=('ltv_cac_ratio', 'mean'),
    avg_soph=('acquisition_sophistication_score', 'mean'),
    avg_eff=('cac_efficiency_percentile', 'mean'),
    avg_chdiv=('channel_diversity_count', 'mean'),
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
    high_cac_rate=('high_cac_alert', 'mean'),
    neg_roi_rate=('negative_roi_alert', 'mean'),
    n_rows=('campaign_id', 'count')
).reset_index()

print(f"\nBy Advertising Channel Type:")
print(channel_analysis.to_string(index=False))

# Analyze by customer_maturity_stage
cust_analysis = df_joined.groupby('customer_maturity_stage').agg(
    avg_cac=('customer_acquisition_cost', 'mean'),
    avg_ltv_cac=('ltv_cac_ratio', 'mean'),
    avg_soph=('acquisition_sophistication_score', 'mean'),
    avg_eff=('cac_efficiency_percentile', 'mean'),
    avg_chdiv=('channel_diversity_count', 'mean'),
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
    high_cac_rate=('high_cac_alert', 'mean'),
    neg_roi_rate=('negative_roi_alert', 'mean'),
    n_rows=('campaign_id', 'count')
).reset_index()

print(f"\nBy Customer Maturity Stage:")
print(cust_analysis.to_string(index=False))

# Analyze by account_maturity_stage
acct_analysis = df_joined.groupby('account_maturity_stage').agg(
    avg_cac=('customer_acquisition_cost', 'mean'),
    avg_ltv_cac=('ltv_cac_ratio', 'mean'),
    avg_soph=('acquisition_sophistication_score', 'mean'),
    avg_eff=('cac_efficiency_percentile', 'mean'),
    avg_chdiv=('channel_diversity_count', 'mean'),
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
    high_cac_rate=('high_cac_alert', 'mean'),
    neg_roi_rate=('negative_roi_alert', 'mean'),
    n_rows=('campaign_id', 'count')
).reset_index()

print(f"\nBy Account Maturity Stage:")
print(acct_analysis.to_string(index=False))

# Analyze by strategic_customer_segment
seg_analysis = df_joined.groupby('strategic_customer_segment').agg(
    avg_cac=('customer_acquisition_cost', 'mean'),
    avg_ltv_cac=('ltv_cac_ratio', 'mean'),
    avg_soph=('acquisition_sophistication_score', 'mean'),
    avg_eff=('cac_efficiency_percentile', 'mean'),
    avg_chdiv=('channel_diversity_count', 'mean'),
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
    high_cac_rate=('high_cac_alert', 'mean'),
    neg_roi_rate=('negative_roi_alert', 'mean'),
    n_rows=('campaign_id', 'count')
).reset_index()

print(f"\nBy Strategic Customer Segment:")
print(seg_analysis.to_string(index=False))

# ===== VISUALIZATIONS =====

# 1. CAC Growth vs LTV/CAC Change scatter plot
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df_camp_metrics['cac_growth'] * 100, df_camp_metrics['ltv_cac_change'] * 100,
                      c=df_camp_metrics['decay_flag'], cmap='RdYlGn_r', s=100, alpha=0.7, edgecolors='black')
plt.axhline(y=-20, color='red', linestyle='--', alpha=0.5, label='LTV/CAC -20% threshold')
plt.axvline(x=25, color='red', linestyle='--', alpha=0.5, label='CAC +25% threshold')
plt.xlabel('CAC Growth Rate (%)', fontsize=12)
plt.ylabel('LTV/CAC Ratio Change (%)', fontsize=12)
plt.title('Campaign Acquisition Efficiency Decay: CAC Growth vs LTV/CAC Change', fontsize=14)
plt.legend(loc='best')
plt.grid(alpha=0.3)
for _, row in df_camp_metrics[df_camp_metrics['decay_flag'] == 1].iterrows():
    plt.annotate(row['account_name'][:12], 
                 (row['cac_growth']*100, row['ltv_cac_change']*100),
                 fontsize=8, ha='left', va='bottom')
plt.tight_layout()
plt.savefig('/work/cac_growth_vs_ltv_cac_change.png', dpi=150)
plt.close()
print("\nSaved: cac_growth_vs_ltv_cac_change.png")

# 2. Risk Score by Campaign
plt.figure(figsize=(12, 6))
camp_names = [f"{r['account_name'][:12]}\n{r['advertising_channel_type'][:8]}" for _, r in df_camp_metrics.iterrows()]
colors = df_camp_metrics['decay_flag'].map({1: '#d73027', 0: '#4575b4'})
bars = plt.bar(range(len(df_camp_metrics)), df_camp_metrics['risk_score'], color=colors, alpha=0.8)
plt.xticks(range(len(df_camp_metrics)), camp_names, rotation=45, ha='right', fontsize=7)
plt.ylabel('Composite Decay Risk Score', fontsize=12)
plt.title('Campaign Decay Risk Assessment', fontsize=14)
plt.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='High Risk Threshold')
plt.axhline(y=0.75, color='red', linestyle='--', alpha=0.5, label='Critical Risk Threshold')
plt.legend()
plt.tight_layout()
plt.savefig('/work/decay_risk_scores.png', dpi=150)
plt.close()
print("Saved: decay_risk_scores.png")

# 3. Multi-dimensional heatmap: Average CAC by lifecycle and channel
heatmap_data = df_joined.pivot_table(
    values='customer_acquisition_cost', 
    index='campaign_lifecycle_stage', 
    columns='advertising_channel_type',
    aggfunc='mean'
)
plt.figure(figsize=(10, 6))
sns.heatmap(heatmap_data, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=0.5)
plt.title('Average CAC by Campaign Lifecycle Stage and Channel Type', fontsize=14)
plt.tight_layout()
plt.savefig('/work/cac_heatmap_lifecycle_channel.png', dpi=150)
plt.close()
print("Saved: cac_heatmap_lifecycle_channel.png")

# 4. LTV/CAC by customer maturity and segment
heatmap2 = df_joined.pivot_table(
    values='ltv_cac_ratio',
    index='customer_maturity_stage',
    columns='strategic_customer_segment',
    aggfunc='mean'
)
plt.figure(figsize=(12, 6))
sns.heatmap(heatmap2, annot=True, fmt='.1f', cmap='RdYlGn', linewidths=0.5, center=10)
plt.title('Average LTV/CAC Ratio by Customer Maturity and Strategic Segment', fontsize=14)
plt.tight_layout()
plt.savefig('/work/ltv_cac_heatmap_maturity_segment.png', dpi=150)
plt.close()
print("Saved: ltv_cac_heatmap_maturity_segment.png")

# 5. Retention risk and scale opportunity by channel
plt.figure(figsize=(10, 6))
retention_by_channel = df_joined.groupby('advertising_channel_type').agg(
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
).reset_index()
x = np.arange(len(retention_by_channel))
width = 0.35
plt.bar(x - width/2, retention_by_channel['retention_risk_rate'] * 100, width, label='Retention Risk %', color='#d73027', alpha=0.7)
plt.bar(x + width/2, retention_by_channel['scale_opp_rate'] * 100, width, label='Scale Opportunity %', color='#1a9850', alpha=0.7)
plt.xticks(x, retention_by_channel['advertising_channel_type'], rotation=45, ha='right')
plt.ylabel('Rate (%)', fontsize=12)
plt.title('Retention Risk and Scale Opportunity by Channel Type', fontsize=14)
plt.legend()
plt.tight_layout()
plt.savefig('/work/retention_scale_by_channel.png', dpi=150)
plt.close()
print("Saved: retention_scale_by_channel.png")

# 6. Acquisition Sophistication vs CAC Efficiency
plt.figure(figsize=(10, 8))
scatter2 = plt.scatter(df_camp_metrics['soph_score_last'], df_camp_metrics['eff_perc_last'],
                       c=df_camp_metrics['risk_score'], cmap='RdYlGn_r', s=100, alpha=0.7, edgecolors='black')
plt.colorbar(scatter2, label='Decay Risk Score')
plt.xlabel('Acquisition Sophistication Score', fontsize=12)
plt.ylabel('CAC Efficiency Percentile', fontsize=12)
plt.title('Sophistication vs Efficiency: Campaign Risk Profile', fontsize=14)
for _, row in df_camp_metrics[df_camp_metrics['decay_flag'] == 1].iterrows():
    plt.annotate(row['account_name'][:10], 
                 (row['soph_score_last'], row['eff_perc_last']),
                 fontsize=8, ha='left', va='bottom')
plt.tight_layout()
plt.savefig('/work/sophistication_vs_efficiency.png', dpi=150)
plt.close()
print("Saved: sophistication_vs_efficiency.png")

# ===== STRATEGIC CUSTOMER SEGMENT ANALYSIS =====
print(f"\n\n=== STRATEGIC CUSTOMER SEGMENT ANALYSIS ===")

# Compute per-segment decay metrics
seg_analysis_detail = df_joined.groupby('strategic_customer_segment').agg(
    avg_cac=('customer_acquisition_cost', 'mean'),
    avg_ltv_cac=('ltv_cac_ratio', 'mean'),
    avg_soph=('acquisition_sophistication_score', 'mean'),
    avg_eff=('cac_efficiency_percentile', 'mean'),
    avg_chdiv=('channel_diversity_count', 'mean'),
    retention_risk_rate=('retention_risk', 'mean'),
    scale_opp_rate=('scale_opportunity', 'mean'),
    high_cac_rate=('high_cac_alert', 'mean'),
    avg_roas=('roas', 'mean'),
    avg_cpc=('cpc', 'mean'),
    avg_payback=('estimated_payback_days', 'mean'),
    n_rows=('campaign_id', 'count')
).reset_index()

seg_analysis_detail['acquisition_efficiency'] = seg_analysis_detail['avg_ltv_cac'] / seg_analysis_detail['avg_cac'].replace(0, np.nan)
print(seg_analysis_detail.to_string(index=False))

# ===== RECOMMENDATIONS =====
print(f"\n\n=== OPTIMIZATION RECOMMENDATIONS ===")

# Summarize by lifecycle stage
for life_stage in df_joined['campaign_lifecycle_stage'].unique():
    subset = df_joined[df_joined['campaign_lifecycle_stage'] == life_stage]
    print(f"\n--- {life_stage} Stage ---")
    print(f"  Avg CAC: {subset['customer_acquisition_cost'].mean():.2f}")
    print(f"  Avg LTV/CAC: {subset['ltv_cac_ratio'].mean():.2f}")
    print(f"  Avg Sophistication: {subset['acquisition_sophistication_score'].mean():.1f}")
    print(f"  Retention Risk Rate: {subset['retention_risk'].mean()*100:.1f}%")
    print(f"  Scale Opportunity Rate: {subset['scale_opportunity'].mean()*100:.1f}%")
    print(f"  Top segments by LTV/CAC:")
    top_seg = subset.groupby('strategic_customer_segment')['ltv_cac_ratio'].mean().sort_values(ascending=False).head(3)
    for seg, val in top_seg.items():
        n = len(subset[subset['strategic_customer_segment'] == seg])
        print(f"    {seg}: {val:.2f} (n={n})")

print(f"\n\n=== SUMMARY STATISTICS ===")
print(f"Total campaigns in analysis: {len(df_camp_metrics)}")
print(f"Campaigns with decay flag: {df_camp_metrics['decay_flag'].sum()}")
print(f"Average CAC growth (all): {df_camp_metrics['cac_growth'].mean()*100:.2f}%")
print(f"Average LTV/CAC change (all): {df_camp_metrics['ltv_cac_change'].mean()*100:.2f}%")
print(f"Average risk score: {df_camp_metrics['risk_score'].mean():.3f}")