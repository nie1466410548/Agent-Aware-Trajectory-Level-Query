SELECT f.feature_id, f.count_visitors,
  dm.month, SUM(dm.count_visitors) AS monthly_visitor_days,
  MAX(dm.count_visitors) AS max_daily_in_month
FROM pendo__feature f
JOIN (
  SELECT feature_id, strftime('%Y-%m', date_day) AS month, count_visitors
  FROM pendo__feature_daily_metrics
) dm ON dm.feature_id = f.feature_id
WHERE f.feature_id IN ('FEAT_00147','FEAT_00081','FEAT_00155','FEAT_00003','FEAT_00109')
GROUP BY f.feature_id, dm.month
ORDER BY f.feature_id, dm.month