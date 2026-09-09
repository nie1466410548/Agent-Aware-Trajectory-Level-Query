-- Campaigns where roas field is nearly constant (low range)
SELECT campaign_id, COUNT(DISTINCT roas) AS distinct_roas, MIN(roas) AS min_roas, MAX(roas) AS max_roas,
  ROUND(MAX(roas) - MIN(roas), 3) AS roas_range,
  ROUND(AVG(roas), 3) AS avg_roas_field,
  ROUND(AVG(conversion_value/NULLIF(cost,0)), 3) AS avg_computed,
  ROUND(AVG(cost), 0) AS avg_monthly_cost
FROM google_ads__campaign_report
GROUP BY campaign_id
HAVING roas_range < 0.1
ORDER BY avg_roas_field