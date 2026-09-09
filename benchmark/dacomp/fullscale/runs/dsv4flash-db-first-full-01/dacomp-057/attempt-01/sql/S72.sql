WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         julianday(substr(a.date_day,1,10)) AS jd, julianday(c.last_date) AS ref_jd,
         a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         a.campaign_lifecycle_stage, a.customer_maturity_stage, a.account_maturity_stage, a.strategic_customer_segment,
         a.acquisition_sophistication_score, a.cac_efficiency_percentile, a.channel_diversity_count,
         a.retention_risk, a.scale_opportunity, a.high_cac_alert, a.negative_roi_alert,
         a.cac_performance_tier, a.acquisition_efficiency_tier, a.acquisition_recommendation
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
)
SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
       SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) AS spend_last,
       SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) AS spend_prior,
       SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) AS conv_prior,
       SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
       SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN acquisition_sophistication_score ELSE 0 END) AS soph_score_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN cac_efficiency_percentile ELSE 0 END) AS eff_perc_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN channel_diversity_count ELSE 0 END) AS ch_div_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN retention_risk ELSE 0 END) AS retention_risk_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN scale_opportunity ELSE 0 END) AS scale_opp_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN high_cac_alert ELSE 0 END) AS high_cac_alert_last,
       MAX(CASE WHEN jd >= ref_jd - 29 THEN negative_roi_alert ELSE 0 END) AS neg_roi_last
FROM joined
GROUP BY campaign_id
HAVING conv_last > 0 AND conv_prior > 0