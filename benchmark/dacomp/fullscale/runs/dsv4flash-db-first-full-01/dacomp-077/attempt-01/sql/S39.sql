WITH monthly AS (
  SELECT feature_id, strftime('%Y-%m', date_day) AS ym,
         MAX(count_visitors) AS max_daily_visitors,
         AVG(count_visitors) AS avg_daily_visitors,
         SUM(count_visitors) AS sum_daily_visitors
  FROM pendo__feature_daily_metrics
  GROUP BY feature_id, strftime('%Y-%m', date_day)
)
SELECT f.feature_id, f.feature_name, f.count_visitors,
       m.ym, m.max_daily_visitors, ROUND(m.avg_daily_visitors,1) AS avg_daily, m.sum_daily_visitors
FROM pendo__feature f
JOIN monthly m ON m.feature_id = f.feature_id
WHERE f.feature_id IN ('FEAT_00155','FEAT_00003','FEAT_00109','FEAT_00121','FEAT_00085')
ORDER BY f.feature_id, m.ym