
SELECT campaign_id, geo_target, ROUND(SUM(cost),0) AS cost,
  ROUND(SUM(conversion_value)/NULLIF(SUM(cost),0), 3) AS computed_roas,
  ROUND(AVG(roas), 3) AS roas_field,
  ROUND(SUM(conversions),2) AS conversions,
  ROUND(SUM(conversion_value),0) AS cv
FROM google_ads__geo_report
WHERE campaign_id IN (105,135,36,184,180,56,69,148,178,27)
GROUP BY campaign_id, geo_target
ORDER BY campaign_id, geo_target
