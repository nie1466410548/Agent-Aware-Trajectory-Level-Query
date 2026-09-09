-- Compare roas field with computed ratio: check if roas field is constant per campaign
SELECT campaign_id, COUNT(DISTINCT roas) AS distinct_roas, MIN(roas) AS min_roas, MAX(roas) AS max_roas,
  ROUND(MAX(roas) - MIN(roas), 3) AS roas_range,
  ROUND(AVG(roas), 3) AS avg_roas_field,
  ROUND(AVG(conversion_value/NULLIF(cost,0)), 3) AS avg_computed
FROM google_ads__campaign_report
GROUP BY campaign_id
ORDER BY roas_range DESC