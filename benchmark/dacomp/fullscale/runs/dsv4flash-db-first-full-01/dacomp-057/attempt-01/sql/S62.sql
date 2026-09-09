WITH camp AS (
  SELECT campaign_id, campaign_name, account_id, account_name, advertising_channel_type, advertising_channel_subtype,
         MAX(substr(date_day,1,10)) AS last_date,
         CAST(julianday(MAX(substr(date_day,1,10))) - julianday(MIN(substr(date_day,1,10))) AS INTEGER) AS days_running
  FROM google_ads__campaign_report
  GROUP BY campaign_id
  HAVING days_running > 120
),
daily AS (
  SELECT c.campaign_id, substr(r.date_day,1,10) AS d, r.spend, r.conversions,
         julianday(substr(r.date_day,1,10)) AS jd
  FROM camp c
  JOIN google_ads__campaign_report r ON r.campaign_id = c.campaign_id
)
SELECT campaign_id,
       SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN spend ELSE 0 END) AS spend_last,
       SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN conversions ELSE 0 END) AS conv_last,
       SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN spend ELSE 0 END) AS spend_prior,
       SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN conversions ELSE 0 END) AS conv_prior,
       ROUND(SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd >= julianday(last_date) - 29 THEN conversions ELSE 0 END),0),2) AS cac_last,
       ROUND(SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN spend ELSE 0 END)/NULLIF(SUM(CASE WHEN jd BETWEEN julianday(last_date) - 59 AND julianday(last_date) - 30 THEN conversions ELSE 0 END),0),2) AS cac_prior
FROM camp c
JOIN daily d USING (campaign_id)
GROUP BY campaign_id
ORDER BY cac_last DESC NULLS LAST