SELECT
  fv.distinct_features,
  COUNT(*) AS n_visitors
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
WHERE v.count_active_days > 60 AND fv.distinct_features < 5
GROUP BY fv.distinct_features
ORDER BY fv.distinct_features