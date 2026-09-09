import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import json, os, warnings
warnings.filterwarnings('ignore')

# Load campaign-level health scores (recompute in SQL)
r = db.query("""
WITH base AS (
  SELECT year_month, campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
    cost, conversions, conversion_value, roas, cpc, cost_per_conversion,
    conversion_rate, quality_score, impression_share, ctr
  FROM google_ads__campaign_report
),
norm AS (
  SELECT *,
    (roas - MIN(roas) OVER()) / NULLIF(MAX(roas) OVER() - MIN(roas) OVER(), 0) AS roas_s,
    (MAX(cpc) OVER() - cpc) / NULLIF(MAX(cpc) OVER() - MIN(cpc) OVER(), 0) AS cpc_s,
    (MAX(cost_per_conversion) OVER() - cost_per_conversion) / NULLIF(MAX(cost_per_conversion) OVER() - MIN(cost_per_conversion) OVER(), 0) AS cpa_s,
    (conversion_rate - MIN(conversion_rate) OVER()) / NULLIF(MAX(conversion_rate) OVER() - MIN(conversion_rate) OVER(), 0) AS cvr_s,
    (conversion_value/NULLIF(conversions,0) - MIN(conversion_value/NULLIF(conversions,0)) OVER()) / NULLIF(MAX(conversion_value/NULLIF(conversions,0)) OVER() - MIN(conversion_value/NULLIF(conversions,0)) OVER(), 0) AS aov_s,
    (conversions - MIN(conversions) OVER()) / NULLIF(MAX(conversions) OVER() - MIN(conversions) OVER(), 0) AS conv_s,
    (quality_score - MIN(quality_score) OVER()) / NULLIF(MAX(quality_score) OVER() - MIN(quality_score) OVER(), 0) AS qs_s,
    (impression_share - MIN(impression_share) OVER()) / NULLIF(MAX(impression_share) OVER() - MIN(impression_share) OVER(), 0) AS is_s,
    (ctr - MIN(ctr) OVER()) / NULLIF(MAX(ctr) OVER() - MIN(ctr) OVER(), 0) AS ctr_s
  FROM base
)
SELECT campaign_id, campaign_name, campaign_type, bidding_strategy, industry,
  COUNT(*) AS n_months,
  AVG(cost) AS avg_monthly_cost,
  SUM(cost) AS total_cost,
  AVG(roas) AS avg_roas,
  AVG(roas_s) AS avg_roas_s,
  AVG(cpc_s) AS avg_cpc_s,
  AVG(cpa_s) AS avg_cpa_s,
  AVG(cvr_s) AS avg_cvr_s,
  AVG(aov_s) AS avg_aov_s,
  AVG(conv_s) AS avg_conv_s,
  AVG(qs_s) AS avg_qs_s,
  AVG(is_s) AS avg_is_s,
  AVG(ctr_s) AS avg_ctr_s,
  100.0 * AVG(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) AS cost_eff,
  100.0 * AVG(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) AS conv_quality,
  100.0 * AVG(0.4*qs_s + 0.3*is_s + 0.3*ctr_s) AS competitive,
  100.0 * AVG(0.4*(0.4*roas_s + 0.3*cpa_s + 0.3*cpc_s) + 0.35*(0.4*cvr_s + 0.3*aov_s + 0.3*conv_s) + 0.25*(0.4*qs_s + 0.3*is_s + 0.3*ctr_s)) AS health_score
FROM norm
GROUP BY campaign_id
ORDER BY health_score
""", parameters=[])
campaigns = db.frame(r)
print("Campaigns shape:", campaigns.shape)
print(campaigns.head(15))

# Define problematic campaigns (those with constant roas < 0.8)
problematic_ids = [105, 135, 36, 184, 180, 56, 69, 148, 178, 27]
campaigns['is_problematic'] = campaigns['campaign_id'].isin(problematic_ids)
print("\n=== Problematic Campaigns ===")
print(campaigns[campaigns['is_problematic']][['campaign_id','campaign_name','campaign_type','bidding_strategy','industry','health_score','cost_eff','conv_quality','competitive','avg_roas','avg_monthly_cost']].to_string(index=False))