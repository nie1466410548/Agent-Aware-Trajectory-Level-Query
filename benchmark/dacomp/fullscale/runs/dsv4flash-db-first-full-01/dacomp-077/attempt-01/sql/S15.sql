SELECT DISTINCT strftime('%Y-%m', date_day) AS month
FROM pendo__feature_daily_metrics
ORDER BY month