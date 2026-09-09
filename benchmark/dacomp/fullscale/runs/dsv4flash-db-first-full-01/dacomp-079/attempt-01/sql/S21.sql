-- Compare the average_daily_minutes distributions
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(MIN(v.average_daily_minutes), 2) AS min_daily_min,
  ROUND(AVG(v.average_daily_minutes), 2) AS avg_daily_min,
  ROUND(MAX(v.average_daily_minutes), 2) AS max_daily_min,
  ROUND(AVG(v.average_daily_events), 2) AS avg_daily_events,
  ROUND(AVG(v.sum_minutes), 2) AS avg_total_minutes,
  ROUND(AVG(v.sum_events), 2) AS avg_total_events,
  ROUND(AVG(v.count_active_days), 2) AS avg_active_days
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment