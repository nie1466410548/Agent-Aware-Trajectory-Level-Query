-- roas distribution
SELECT 
  CASE 
    WHEN roas < 0.3 THEN '<0.3'
    WHEN roas < 0.5 THEN '0.3-0.5'
    WHEN roas < 0.7 THEN '0.5-0.7'
    WHEN roas < 0.8 THEN '0.7-0.8'
    WHEN roas < 1.0 THEN '0.8-1.0'
    WHEN roas < 2.0 THEN '1.0-2.0'
    ELSE '2.0+'
  END AS roas_range,
  COUNT(*) AS n,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER(), 1) AS pct,
  ROUND(AVG(cost), 0) AS avg_cost,
  ROUND(AVG(conversion_value), 0) AS avg_cv
FROM google_ads__campaign_report
GROUP BY roas_range
ORDER BY MIN(roas)