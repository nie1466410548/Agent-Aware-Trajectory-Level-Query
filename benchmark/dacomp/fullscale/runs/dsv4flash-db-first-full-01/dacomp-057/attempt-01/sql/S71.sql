WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MIN(substr(date_day,1,10)) AS first_date, MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
)
SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.days_running,
       c.last_date AS camp_last_date,
       a.date_day, a.campaign_lifecycle_stage, a.advertising_channel_type, a.advertising_channel_subtype,
       a.customer_maturity_stage, a.account_maturity_stage, a.strategic_customer_segment,
       a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions, a.conversions_value,
       a.acquisition_sophistication_score, a.cac_efficiency_percentile, a.channel_diversity_count,
       a.retention_risk, a.scale_opportunity, a.high_cac_alert, a.negative_roi_alert,
       a.cac_performance_tier, a.acquisition_efficiency_tier, a.acquisition_recommendation,
       a.roas, a.cpc, a.ctr, a.estimated_payback_days,
       a.active_campaigns_count, a.cumulative_acquisition_cost, a.cumulative_conversions, a.cumulative_ltv,
       a.cac_vs_cohort_pct, a.ltv_vs_cohort_pct,
       julianday(substr(a.date_day,1,10)) AS jd
FROM camp c
JOIN google_ads__customer_acquisition_analysis a
  ON a.account_id = c.account_id
 AND a.advertising_channel_type = c.advertising_channel_type
 AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
 AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
ORDER BY c.campaign_id, a.date_day