-- Compare average_daily_minutes by segment through distribution quantiles
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.average_daily_minutes), 2) AS mean,
  ROUND(AVG(CASE WHEN v.count_active_days > 60 THEN v.average_daily_minutes END), 2) AS mean_among_active
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment