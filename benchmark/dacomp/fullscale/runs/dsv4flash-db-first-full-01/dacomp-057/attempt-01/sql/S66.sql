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
)
SELECT campaign_id, campaign_name, account_id, advertising_channel_type, advertising_channel_subtype,
       ROUND(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END),0),2) AS cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END),0),2) AS cac_prior,
       ROUND(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions*ltv_cac_ratio ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END),0),2) AS ltv_cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions*ltv_cac_ratio ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END),0),2) AS ltv_cac_prior
FROM joined
GROUP BY campaign_id
HAVING SUM(CASE WHEN jd >= julianday('2024-12-31') - 29 THEN conversions ELSE 0 END) > 0
   AND SUM(CASE WHEN jd BETWEEN julianday('2024-12-31') - 59 AND julianday('2024-12-31') - 30 THEN conversions ELSE 0 END) > 0
ORDER BY campaign_id