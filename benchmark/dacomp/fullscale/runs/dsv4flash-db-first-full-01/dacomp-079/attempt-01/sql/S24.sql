SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(v.count_active_months), 2) AS avg_active_months,
  ROUND(AVG(julianday(v.last_event_on) - julianday(v.first_event_on)), 1) AS avg_span_days,
  ROUND(AVG(v.count_active_months * 1.0 / NULLIF(ROUND((julianday(v.last_event_on) - julianday(v.first_event_on)) / 30.0), 0)), 4) AS avg_months_coverage_ratio
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
GROUP BY segment