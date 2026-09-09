SELECT
  f.feature_id,
  f.feature_name,
  f.count_visitors,
  ROUND(AVG(fdm.count_visitors), 1) AS avg_daily_visitors,
  ROUND(AVG(fdm.count_visitors) * 30.4, 1) AS est_monthly_visitors,
  f.product_area_name
FROM pendo__feature f
JOIN pendo__feature_daily_metrics fdm ON fdm.feature_id = f.feature_id
WHERE f.count_visitors < 300
GROUP BY f.feature_id
ORDER BY f.count_visitors DESC
LIMIT 30