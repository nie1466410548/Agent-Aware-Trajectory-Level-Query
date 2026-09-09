WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
joined AS (
  SELECT c.campaign_id, c.campaign_name, c.account_id, c.account_name, c.advertising_channel_type, c.advertising_channel_subtype,
         substr(a.date_day,1,10) AS d, a.customer_acquisition_cost, a.ltv_cac_ratio, a.spend, a.conversions,
         julianday(substr(a.date_day,1,10)) AS jd, julianday(c.last_date) AS ref_jd
  FROM camp c
  JOIN google_ads__customer_acquisition_analysis a
    ON a.account_id = c.account_id
   AND a.advertising_channel_type = c.advertising_channel_type
   AND COALESCE(a.advertising_channel_subtype,'') = COALESCE(c.advertising_channel_subtype,'')
   AND substr(a.date_day,1,10) BETWEEN c.first_date AND c.last_date
),
metrics AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN spend ELSE 0 END) AS spend_last,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions ELSE 0 END) AS conv_last,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN spend ELSE 0 END) AS spend_prior,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions ELSE 0 END) AS conv_prior,
         SUM(CASE WHEN jd >= ref_jd - 29 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_last,
         SUM(CASE WHEN jd BETWEEN ref_jd - 59 AND ref_jd - 30 THEN conversions*ltv_cac_ratio ELSE 0 END) AS ltv_cac_w_prior
  FROM joined
  GROUP BY campaign_id
  HAVING conv_last > 0 AND conv_prior > 0
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       ROUND((spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior),4) AS cac_growth,
       ROUND((ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior),4) AS ltv_cac_change,
       CASE WHEN (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) > 0.25 
            AND (ltv_cac_w_last/conv_last - ltv_cac_w_prior/conv_prior)/(ltv_cac_w_prior/conv_prior) < -0.20
       THEN 'DECAY_FLAG' ELSE 'ok' END AS status
FROM metrics
ORDER BY (spend_last/conv_last - spend_prior/conv_prior)/(spend_prior/conv_prior) DESC