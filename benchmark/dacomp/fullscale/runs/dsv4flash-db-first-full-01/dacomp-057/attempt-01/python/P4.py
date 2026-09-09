import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os

# ===== LOAD DATA =====
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
df_joined = pd.DataFrame(load_rows('/results/S71.rows.jsonl'), columns=cols71)

cols72 = ["campaign_id","campaign_name","account_id","account_name","advertising_channel_type","advertising_channel_subtype",
          "spend_last","conv_last","spend_prior","conv_prior","ltv_cac_w_last","ltv_cac_w_prior",
          "soph_score_last","eff_perc_last","ch_div_last","retention_risk_last","scale_opp_last",
          "high_cac_alert_last","neg_roi_last"]
df_camp = pd.DataFrame(load_rows('/results/S72.rows.jsonl'), columns=cols72)

# ===== CAMPAIGN-LEVEL DECAY METRICS =====
df_camp['cac_last'] = df_camp['spend_last'] / df_camp['conv_last'].replace(0, np.nan)
df_camp['cac_prior'] = df_camp['spend_prior'] / df_camp['conv_prior'].replace(0, np.nan)
df_camp['ltv_cac_last'] = df_camp['ltv_cac_w_last'] / df_camp['conv_last'].replace(0, np.nan)
df_camp['ltv_cac_prior'] = df_camp['ltv_cac_w_prior'] / df_camp['conv_prior'].replace(0, np.nan)
df_camp['cac_growth'] = (df_camp['cac_last'] - df_camp['cac_prior']) / df_camp['cac_prior'].replace(0, np.nan)
df_camp['ltv_cac_change'] = (df_camp['ltv_cac_last'] - df_camp['ltv_cac_prior']) / df_camp['ltv_cac_prior'].replace(0, np.nan)
df_camp['decay_flag'] = ((df_camp['cac_growth'] > 0.25) & (df_camp['ltv_cac_change'] < -0.20)).astype(int)

print("=== CAMPAIGN DECAY ANALYSIS ===")
print(f"Total campaigns with sufficient data: {len(df_camp)}")
print(f"Campaigns with CAC growth >25% and LTV/CAC decline >20%: {df_camp['decay_flag'].sum()}")
decay_camps = df_camp[df_camp['decay_flag'] == 1]
for _, row in decay_camps.iterrows():
    print(f"  {row['campaign_id']} ({row['account_name']}) - {row['advertising_channel_type']}/{row['advertising_channel_subtype']}")
    print(f"    CAC: {row['cac_prior']:.2f} -> {row['cac_last']:.2f} (growth: {row['cac_growth']*100:.1f}%)")
    print(f"    LTV/CAC: {row['ltv_cac_prior']:.2f} -> {row['ltv_cac_last']:.2f} (change: {row['ltv_cac_change']*100:.1f}%)")

# ===== DECAY RISK MODEL =====
print("\n\n=== DECAY RISK MODEL ===")

# Normalize and compute composite risk score
max_cac_growth = df_camp['cac_growth'].max()
df_camp['cac_growth_risk'] = df_camp['cac_growth'].clip(0) / max_cac_growth if max_cac_growth > 0 else 0

min_ltv_change = df_camp['ltv_cac_change'].min()
df_camp['ltv_decline_risk'] = (-df_camp['ltv_cac_change'].clip(upper=0)) / (-min_ltv_change) if min_ltv_change < 0 else 0

max_soph, min_soph = df_camp['soph_score_last'].max(), df_camp['soph_score_last'].min()
df_camp['soph_risk'] = 1 - (df_camp['soph_score_last'] - min_soph) / (max_soph - min_soph) if max_soph > min_soph else 0

max_eff, min_eff = df_camp['eff_perc_last'].max(), df_camp['eff_perc_last'].min()
df_camp['eff_risk'] = 1 - (df_camp['eff_perc_last'] - min_eff) / (max_eff - min_eff) if max_eff > min_eff else 0

max_ch, min_ch = df_camp['ch_div_last'].max(), df_camp['ch_div_last'].min()
df_camp['ch_div_risk'] = 1 - (df_camp['ch_div_last'] - min_ch) / (max_ch - min_ch) if max_ch > min_ch else 0

max_ret = df_camp['retention_risk_last'].max()
df_camp['retention_risk_norm'] = df_camp['retention_risk_last'] / max_ret if max_ret > 0 else 0

df_camp['risk_score'] = (
    0.25 * df_camp['cac_growth_risk'] + 0.25 * df_camp['ltv_decline_risk'] +
    0.15 * df_camp['soph_risk'] + 0.15 * df_camp['eff_risk'] +
    0.10 * df_camp['ch_div_risk'] + 0.10 * df_camp['retention_risk_norm']
)

df_camp['risk_tier'] = pd.cut(df_camp['risk_score'],
                              bins=[-0.001, 0.25, 0.5, 0.75, 1.001],
                              labels=['Low', 'Medium', 'High', 'Critical'])

print("Risk tier distribution:")
print(df_camp['risk_tier'].value_counts().sort_index())

print("\nHigh/Critical risk campaigns:")
for _, row in df_camp[df_camp['risk_tier'].isin(['High', 'Critical'])].sort_values('risk_score', ascending=False).iterrows():
    print(f"  {row['campaign_id']} ({row['account_name']}) - {row['advertising_channel_type']}")
    print(f"    Risk Score: {row['risk_score']:.3f}, Tier: {row['risk_tier']}")
    print(f"    CAC Growth: {row['cac_growth']*100:.1f}%, LTV/CAC Change: {row['ltv_cac_change']*100:.1f}%")

# ===== SEGMENT-LEVEL ANALYSIS =====
print("\n\n=== SEGMENT-LEVEL ANALYSIS ===")

# By campaign lifecycle stage
lc_groups = df_joined.groupby('campaign_lifecycle_stage')
print("\n--- By Campaign Lifecycle Stage ---")
for name, grp in lc_groups:
    print(f"  {name}: n={len(grp)}, Avg CAC={grp['customer_acquisition_cost'].mean():.2f}, "
          f"Avg LTV/CAC={grp['ltv_cac_ratio'].mean():.2f}, "
          f"Avg Soph={grp['acquisition_sophistication_score'].mean():.1f}, "
          f"Avg Eff={grp['cac_efficiency_percentile'].mean():.1f}, "
          f"Retention Risk={grp['retention_risk'].mean()*100:.1f}%, "
          f"Scale Opp={grp['scale_opportunity'].mean()*100:.1f}%")

# By channel
ch_groups = df_joined.groupby('advertising_channel_type')
print("\n--- By Advertising Channel ---")
for name, grp in ch_groups:
    print(f"  {name}: n={len(grp)}, Avg CAC={grp['customer_acquisition_cost'].mean():.2f}, "
          f"Avg LTV/CAC={grp['ltv_cac_ratio'].mean():.2f}, "
          f"Avg Soph={grp['acquisition_sophistication_score'].mean():.1f}, "
          f"Avg Eff={grp['cac_efficiency_percentile'].mean():.1f}, "
          f"Retention Risk={grp['retention_risk'].mean()*100:.1f}%")

# By customer maturity
cust_groups = df_joined.groupby('customer_maturity_stage')
print("\n--- By Customer Maturity Stage ---")
for name, grp in cust_groups:
    print(f"  {name}: n={len(grp)}, Avg CAC={grp['customer_acquisition_cost'].mean():.2f}, "
          f"Avg LTV/CAC={grp['ltv_cac_ratio'].mean():.2f}, "
          f"Avg Soph={grp['acquisition_sophistication_score'].mean():.1f}")

# By account maturity
acct_groups = df_joined.groupby('account_maturity_stage')
print("\n--- By Account Maturity Stage ---")
for name, grp in acct_groups:
    print(f"  {name}: n={len(grp)}, Avg CAC={grp['customer_acquisition_cost'].mean():.2f}, "
          f"Avg LTV/CAC={grp['ltv_cac_ratio'].mean():.2f}, "
          f"Avg Soph={grp['acquisition_sophistication_score'].mean():.1f}")

# By strategic customer segment
seg_groups = df_joined.groupby('strategic_customer_segment')
print("\n--- By Strategic Customer Segment ---")
for name, grp in seg_groups:
    print(f"  {name}: n={len(grp)}, Avg CAC={grp['customer_acquisition_cost'].mean():.2f}, "
          f"Avg LTV/CAC={grp['ltv_cac_ratio'].mean():.2f}, "
          f"Avg Soph={grp['acquisition_sophistication_score'].mean():.1f}, "
          f"Retention Risk={grp['retention_risk'].mean()*100:.1f}%, "
          f"Scale Opp={grp['scale_opportunity'].mean()*100:.1f}%")

# ===== VISUALIZATIONS =====

# 1. CAC Growth vs LTV/CAC Change
plt.figure(figsize=(10, 8))
scatter = plt.scatter(df_camp['cac_growth']*100, df_camp['ltv_cac_change']*100,
                      c=df_camp['decay_flag'], cmap='RdYlGn_r', s=100, alpha=0.7, edgecolors='black')
plt.axhline(y=-20, color='red', linestyle='--', alpha=0.5, label='LTV/CAC -20% threshold')
plt.axvline(x=25, color='red', linestyle='--', alpha=0.5, label='CAC +25% threshold')
plt.xlabel('CAC Growth Rate (%)')
plt.ylabel('LTV/CAC Ratio Change (%)')
plt.title('Campaign Acquisition Efficiency Decay')
plt.legend()
plt.grid(alpha=0.3)
for _, row in df_camp[df_camp['decay_flag']==1].iterrows():
    plt.annotate(row['account_name'][:12], (row['cac_growth']*100, row['ltv_cac_change']*100),
                 fontsize=8, ha='left', va='bottom')
plt.tight_layout()
plt.savefig('/work/cac_growth_vs_ltv_cac_change.png', dpi=150)
plt.close()

# 2. Risk Scores
plt.figure(figsize=(12, 6))
labels = [f"{r['account_name'][:10]}\n{r['advertising_channel_type'][:6]}" for _, r in df_camp.iterrows()]
colors = ['#d73027' if f else '#4575b4' for f in df_camp['decay_flag']]
plt.bar(range(len(df_camp)), df_camp['risk_score'], color=colors, alpha=0.8)
plt.xticks(range(len(df_camp)), labels, rotation=45, ha='right', fontsize=6)
plt.ylabel('Composite Decay Risk Score')
plt.title('Campaign Decay Risk Assessment')
plt.axhline(y=0.5, color='orange', linestyle='--', alpha=0.5, label='High Risk')
plt.axhline(y=0.75, color='red', linestyle='--', alpha=0.5, label='Critical Risk')
plt.legend()
plt.tight_layout()
plt.savefig('/work/decay_risk_scores.png', dpi=150)
plt.close()

# 3. CAC Heatmap by Lifecycle and Channel
pivot_cac = df_joined.pivot_table(values='customer_acquisition_cost', 
                                   index='campaign_lifecycle_stage', 
                                   columns='advertising_channel_type', aggfunc='mean')
plt.figure(figsize=(10, 6))
sns.heatmap(pivot_cac, annot=True, fmt='.1f', cmap='YlOrRd', linewidths=0.5)
plt.title('Average CAC by Lifecycle Stage and Channel Type')
plt.tight_layout()
plt.savefig('/work/cac_heatmap_lifecycle_channel.png', dpi=150)
plt.close()

# 4. LTV/CAC Heatmap
pivot_ltv = df_joined.pivot_table(values='ltv_cac_ratio',
                                   index='customer_maturity_stage',
                                   columns='strategic_customer_segment', aggfunc='mean')
plt.figure(figsize=(12, 6))
sns.heatmap(pivot_ltv, annot=True, fmt='.1f', cmap='RdYlGn', linewidths=0.5, center=10)
plt.title('Average LTV/CAC by Customer Maturity and Strategic Segment')
plt.tight_layout()
plt.savefig('/work/ltv_cac_heatmap_maturity_segment.png', dpi=150)
plt.close()

# 5. Retention Risk and Scale Opportunity by Channel
ret_ch = df_joined.groupby('advertising_channel_type')[['retention_risk','scale_opportunity']].mean().reset_index()
plt.figure(figsize=(10, 6))
x = np.arange(len(ret_ch))
width = 0.35
plt.bar(x - width/2, ret_ch['retention_risk']*100, width, label='Retention Risk %', color='#d73027', alpha=0.7)
plt.bar(x + width/2, ret_ch['scale_opportunity']*100, width, label='Scale Opportunity %', color='#1a9850', alpha=0.7)
plt.xticks(x, ret_ch['advertising_channel_type'], rotation=45, ha='right')
plt.ylabel('Rate (%)')
plt.title('Retention Risk and Scale Opportunity by Channel Type')
plt.legend()
plt.tight_layout()
plt.savefig('/work/retention_scale_by_channel.png', dpi=150)
plt.close()

# 6. Sophistication vs Efficiency
plt.figure(figsize=(10, 8))
scatter2 = plt.scatter(df_camp['soph_score_last'], df_camp['eff_perc_last'],
                       c=df_camp['risk_score'], cmap='RdYlGn_r', s=100, alpha=0.7, edgecolors='black')
plt.colorbar(scatter2, label='Decay Risk Score')
plt.xlabel('Acquisition Sophistication Score')
plt.ylabel('CAC Efficiency Percentile')
plt.title('Campaign Risk Profile: Sophistication vs Efficiency')
for _, row in df_camp[df_camp['decay_flag']==1].iterrows():
    plt.annotate(row['account_name'][:10], (row['soph_score_last'], row['eff_perc_last']),
                 fontsize=8, ha='left', va='bottom')
plt.tight_layout()
plt.savefig('/work/sophistication_vs_efficiency.png', dpi=150)
plt.close()

print("\n\nAll visualizations saved successfully.")

# ===== FINAL SUMMARY =====
print("\n\n=== FINAL ANALYSIS SUMMARY ===")
print(f"Total long-running campaigns (>120 days): 77")
print(f"Campaigns with sufficient acquisition data (joined): 61")
print(f"Campaigns with valid 30-day window comparison: {len(df_camp)}")
print(f"Campaigns flagged for decay: {df_camp['decay_flag'].sum()}")
print(f"  - CMP_ACC_FIN_001_003, CMP_ACC_FIN_001_007 (SmartInvest App, SHOPPING)")
print(f"  - CMP_ACC_ECOM_002_002 (FashionForward, VIDEO/YOUTUBE_SEARCH)")
print(f"Average CAC growth across all campaigns: {df_camp['cac_growth'].mean()*100:.1f}%")
print(f"Average LTV/CAC change across all campaigns: {df_camp['ltv_cac_change'].mean()*100:.1f}%")
print(f"Average risk score: {df_camp['risk_score'].mean():.3f}")
print(f"High/Critical risk campaigns: {len(df_camp[df_camp['risk_tier'].isin(['High','Critical'])])}")