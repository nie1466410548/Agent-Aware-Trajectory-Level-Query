SELECT
  COUNT(*) AS total_vf,
  COUNT(DISTINCT visitor_id) AS n_visitors_used,
  COUNT(DISTINCT feature_id) AS n_features_used
FROM pendo__visitor_feature