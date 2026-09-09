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

decay_zones = [
    ('ACC_FIN_001','SHOPPING','SHOPPING_GOAL_OPTIMIZED_ADS'),
    ('ACC_ECOM_002','VIDEO','YOUTUBE_SEARCH')
]
df['is_decay_zone'] = df.apply(lambda r: (r['account_id'], r['advertising_channel_type'], r['advertising_channel_subtype']) in decay_zones, axis=1)
df['date_dt'] = pd.to_datetime(df['date_day'].str[:10])
df['ym'] = df['date_dt'].dt.to_period('M').astype(str)

dz = df[df['is_decay_zone']]
hz = df[~df['is_decay_zone']]

trend_dz = dz.groupby('ym').agg(cac=('customer_acquisition_cost','mean'), ltv_cac=('ltv_cac_ratio','mean')).reset_index()
trend_hz = hz.groupby('ym').agg(cac=('customer_acquisition_cost','mean'), ltv_cac=('ltv_cac_ratio','mean')).reset_index()

trend_dz = trend_dz[(trend_dz['ym']>='2024-01') & (trend_dz['ym']<='2024-12')]
trend_hz = trend_hz[(trend_hz['ym']>='2024-01') & (trend_hz['ym']<='2024-12')]

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
axes[0].plot(trend_dz['ym'], trend_dz['cac'], marker='o', color='#d73027', label='Decayed zones')
axes[0].plot(trend_hz['ym'], trend_hz['cac'], marker='o', color='#4575b4', label='Healthy zones')
axes[0].set_xticks(trend_dz['ym'][::2])
axes[0].set_xticklabels(trend_dz['ym'][::2], rotation=45, fontsize=8)
axes[0].set_title('CAC Monthly Trend (2024)')
axes[0].set_ylabel('Avg CAC')
axes[0].legend()
axes[0].grid(alpha=0.3)

axes[1].plot(trend_dz['ym'], trend_dz['ltv_cac'], marker='o', color='#d73027', label='Decayed zones')
axes[1].plot(trend_hz['ym'], trend_hz['ltv_cac'], marker='o', color='#4575b4', label='Healthy zones')
axes[1].set_xticks(trend_dz['ym'][::2])
axes[1].set_xticklabels(trend_dz['ym'][::2], rotation=45, fontsize=8)
axes[1].set_title('LTV/CAC Monthly Trend (2024)')
axes[1].set_ylabel('Avg LTV/CAC')
axes[1].legend()
axes[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/decay_zone_trend_2024.png', dpi=150)
plt.close()
print("Saved: decay_zone_trend_2024.png")
print("Decayed zones monthly CAC (2024):")
print(trend_dz.to_string(index=False))

# ===== RISK MODEL DRIVER ANALYSIS =====
cols72 = ["campaign_id","campaign_name","account_id","account_name","advertising_channel_type","advertising_channel_subtype",
          "spend_last","conv_last","spend_prior","conv_prior","ltv_cac_w_last","ltv_cac_w_prior",
          "soph_score_last","eff_perc_last","ch_div_last","retention_risk_last","scale_opp_last",
          "high_cac_alert_last","neg_roi_last"]
df_camp = pd.DataFrame(load_rows('/results/S72.rows.jsonl'), columns=cols72)
df_camp['cac_last'] = df_camp['spend_last']/df_camp['conv_last']
df_camp['cac_prior'] = df_camp['spend_prior']/df_camp['conv_prior']
df_camp['ltv_cac_last'] = df_camp['ltv_cac_w_last']/df_camp['conv_last']
df_camp['ltv_cac_prior'] = df_camp['ltv_cac_w_prior']/df_camp['conv_prior']
df_camp['cac_growth'] = (df_camp['cac_last']-df_camp['cac_prior'])/df_camp['cac_prior']
df_camp['ltv_cac_change'] = (df_camp['ltv_cac_last']-df_camp['ltv_cac_prior'])/df_camp['ltv_cac_prior']
df_camp['decay_flag'] = ((df_camp['cac_growth']>0.25)&(df_camp['ltv_cac_change']<-0.20)).astype(int)

print("\n=== RISK FACTOR CORRELATION WITH DECAY FLAG ===")
factors = ['cac_growth','ltv_cac_change','soph_score_last','eff_perc_last','ch_div_last','retention_risk_last','scale_opp_last']
for f in factors:
    corr = df_camp[f].corr(df_camp['decay_flag'])
    print(f"  {f}: r = {corr:.3f}")

print("\n=== FACTOR PROFILE: Decayed vs Healthy Campaigns ===")
prof_dec = df_camp[df_camp['decay_flag']==1][factors].mean().round(2)
prof_hea = df_camp[df_camp['decay_flag']==0][factors].mean().round(2)
print(pd.DataFrame({'Decayed': prof_dec, 'Healthy': prof_hea}).to_string())

print("\n=== ACQUISITION RECOMMENDATIONS (decay zones) ===")
print(dz.groupby('acquisition_recommendation').agg(n=('campaign_id','count'), avg_cac=('customer_acquisition_cost','mean')).to_string())
print("\n=== ACQUISITION RECOMMENDATIONS (healthy zones) ===")
print(hz.groupby('acquisition_recommendation').agg(n=('campaign_id','count'), avg_cac=('customer_acquisition_cost','mean')).to_string())

print("\n=== EFFICIENCY TIER (decay zones) ===")
print(dz.groupby('acquisition_efficiency_tier').agg(n=('campaign_id','count'), avg_cac=('customer_acquisition_cost','mean')).to_string())
print("\n=== CAC PERFORMANCE TIER (decay zones) ===")
print(dz.groupby('cac_performance_tier').agg(n=('campaign_id','count'), avg_cac=('customer_acquisition_cost','mean')).to_string())

plt.figure(figsize=(10, 6))
driver_corr = [df_camp[f].corr(df_camp['decay_flag']) for f in factors]
colors = ['#d73027' if c>0 else '#4575b4' for c in driver_corr]
plt.barh(factors, driver_corr, color=colors, alpha=0.8)
plt.xlabel('Correlation with Decay Flag')
plt.title('Risk Model Drivers: Correlation with CAC Decay Flag')
plt.axvline(x=0, color='black', linewidth=0.8)
plt.tight_layout()
plt.savefig('/work/risk_drivers.png', dpi=150)
plt.close()
print("Saved: risk_drivers.png")