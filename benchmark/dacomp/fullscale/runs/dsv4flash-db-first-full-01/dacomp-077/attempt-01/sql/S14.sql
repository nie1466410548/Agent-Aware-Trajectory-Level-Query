SELECT
  s.strftime_Y_m AS month,
  COUNT(DISTINCT date_day) AS days_in_month
FROM (
  SELECT DISTINCT strftime('%Y-%m', date_day) AS strftime_Y_m
  FROM pendo__feature_daily_metrics
) s
GROUP BY s.strftime_Y_m
ORDER BY s.strftime_Y_m