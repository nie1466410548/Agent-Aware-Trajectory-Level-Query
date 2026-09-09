SELECT
  feature_id,
  feature_name,
  COUNT(DISTINCT strftime('%Y-%m', date_day)) AS n_months,
  AVG(count_visitors) AS avg_daily_visitors,
  MAX(count_visitors) AS max_daily_visitors,
  SUM(count_visitors) AS sum_daily_visitors
FROM pendo__feature_daily_metrics
GROUP BY feature_id
ORDER BY avg_daily_visitors ASC
LIMIT 20