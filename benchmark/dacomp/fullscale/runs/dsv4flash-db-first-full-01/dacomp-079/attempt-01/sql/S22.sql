SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months,
  ROUND(AVG(CAST(julianday(COALESCE(v.last_event_on, v.last_visit)) - julianday(COALESCE(v.first_event_on, v.first_visit_at)) AS REAL)), 1) AS avg_tenure_days,
  ROUND(AVG(CASE WHEN julianday(COALESCE(v.last_event_on, v.last_visit)) < julianday('2025-10-14') - 90 THEN 1 ELSE 0 END), 4) AS churn_rate_90d
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment