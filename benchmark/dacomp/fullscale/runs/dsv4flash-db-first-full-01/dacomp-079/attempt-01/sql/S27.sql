-- Retention proxy: recency of last event
SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(julianday('2025-10-14') - julianday(v.last_event_on)), 1) AS avg_days_since_last_event,
  ROUND(AVG(julianday('2025-10-14') - julianday(v.first_event_on)), 1) AS avg_days_since_first_event
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment