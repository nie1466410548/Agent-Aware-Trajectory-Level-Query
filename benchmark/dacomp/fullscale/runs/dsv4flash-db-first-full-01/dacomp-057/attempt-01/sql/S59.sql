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
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         a.campaign_lifecycle_stage, a.customer_maturity_stage, a.account_maturity_stage, a.strategic_customer_segment,
         a.acquisition_sophistication_score, a.cac_efficiency_percentile, a.channel_diversity_count,
         a.retention_risk, a.scale_opportunity, a.high_cac_alert, a.negative_roi_alert,
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
refs AS (
  SELECT campaign_id, MAX(jd) AS ref_jd, MAX(d) AS ref_date, COUNT(*) AS n_rows,
         MAX(jd) - MIN(jd) AS span_days
  FROM joined
  GROUP BY campaign_id
)
SELECT j.campaign_id, j.campaign_name, j.account_id, j.advertising_channel_type, j.advertising_channel_subtype,
       r.ref_date, r.span_days,
       SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN 1 ELSE 0 END) AS n_last30,
       SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN 1 ELSE 0 END) AS n_prior30
FROM joined j
JOIN refs r ON r.campaign_id = j.campaign_id
GROUP BY j.campaign_id
ORDER BY r.ref_date DESC