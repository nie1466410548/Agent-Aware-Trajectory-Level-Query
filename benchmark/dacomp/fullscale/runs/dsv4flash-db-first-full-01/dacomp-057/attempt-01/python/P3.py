import numpy as np
import pandas as pd
import json

def load_rows(path):
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

data_joined = load_rows('/results/S71.rows.jsonl')
data_metrics = load_rows('/results/S72.rows.jsonl')

cols71 = ["campaign_id","campaign_name","account_id","account_name","days_running","camp_last_date","date_day",
          "campaign_lifecycle_stage","advertising_channel_type","advertising_channel_subtype","customer_maturity_stage",
          "account_maturity_stage","strategic_customer_segment","customer_acquisition_cost","ltv_cac_ratio","spend",
          "conversions","conversions_value","acquisition_sophistication_score","cac_efficiency_percentile",
          "channel_diversity_count","retention_risk","scale_opportunity","high_cac_alert","negative_roi_alert",
          "cac_performance_tier","acquisition_efficiency_tier","acquisition_recommendation","roas","cpc","ctr",
          "estimated_payback_days","active_campaigns_count","cumulative_acquisition_cost","cumulative_conversions",
          "cumulative_ltv","cac_vs_cohort_pct","ltv_vs_cohort_pct","jd"]
df_joined = pd.DataFrame(data_joined, columns=cols71)

cols72 = ["campaign_id","campaign_name","account_id","account_name","advertising_channel_type","advertising_channel_subtype",
          "spend_last","conv_last","spend_prior","conv_prior","ltv_cac_w_last","ltv_cac_w_prior",
          "soph_score_last","eff_perc_last","ch_div_last","retention_risk_last","scale_opp_last",
          "high_cac_alert_last","neg_roi_last"]
df_camp_metrics = pd.DataFrame(data_metrics, columns=cols72)

print(f"Joined rows: {len(df_joined)}")
print(f"Campaign metrics rows: {len(df_camp_metrics)}")
print("S71 sample:")
print(df_joined[['campaign_id','account_name','campaign_lifecycle_stage','customer_acquisition_cost','ltv_cac_ratio']].head(3))
print("S72 sample:")
print(df_camp_metrics[['campaign_id','account_name','spend_last','conv_last']].head(3))