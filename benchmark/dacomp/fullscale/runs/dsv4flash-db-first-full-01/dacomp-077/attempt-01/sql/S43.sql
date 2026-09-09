SELECT
  AVG(vf_count) AS avg_features_per_visitor,
  MIN(vf_count) AS min_features,
  MAX(vf_count) AS max_features,
  MEDIAN(vf_count) AS median_features
FROM (
  SELECT visitor_id, COUNT(*) AS vf_count
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) t