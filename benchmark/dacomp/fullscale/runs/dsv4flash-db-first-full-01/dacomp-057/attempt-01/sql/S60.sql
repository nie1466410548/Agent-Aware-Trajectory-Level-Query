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
         julianday(substr(a.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
refs AS (
  SELECT campaign_id, MAX(jd) AS ref_jd FROM joined GROUP BY campaign_id
),
win AS (
  SELECT j.campaign_id, j.campaign_name, j.account_id, j.account_name, j.advertising_channel_type, j.advertising_channel_subtype,
         r.ref_jd,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN j.jd >= r.ref_jd - 29 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN j.jd BETWEEN r.ref_jd - 59 AND r.ref_jd - 30 THEN j.conversions * j.ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined j
  JOIN refs r ON r.campaign_id = j.campaign_id
  GROUP BY j.campaign_id
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       spend_last, conv_last, spend_prior, conv_prior,
       ROUND(spend_last/NULLIF(conv_last,0),2) AS cac_last,
       ROUND(spend_prior/NULLIF(conv_prior,0),2) AS cac_prior,
       ROUND((spend_last/NULLIF(conv_last,0) - spend_prior/NULLIF(conv_prior,0))/NULLIF(spend_prior/NULLIF(conv_prior,0),0),4) AS cac_growth,
       ROUND(ltv_cac_w_last/NULLIF(conv_last,0),2) AS ltv_cac_last,
       ROUND(ltv_cac_w_prior/NULLIF(conv_prior,0),2) AS ltv_cac_prior,
       ROUND((ltv_cac_w_last/NULLIF(conv_last,0) - ltv_cac_w_prior/NULLIF(conv_prior,0))/NULLIF(ltv_cac_w_prior/NULLIF(conv_prior,0),0),4) AS ltv_cac_change
FROM win
ORDER BY cac_growth DESC