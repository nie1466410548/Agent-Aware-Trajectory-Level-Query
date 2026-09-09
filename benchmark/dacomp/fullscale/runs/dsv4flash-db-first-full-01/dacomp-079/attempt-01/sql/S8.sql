SELECT COUNT(*) AS total_visitors,
  SUM(CASE WHEN count_active_days > 60 THEN 1 ELSE 0 END) AS active_gt_60,
  SUM(CASE WHEN count_active_days > 60 AND (SELECT COUNT(DISTINCT feature_id) FROM pendo__visitor_feature vf WHERE vf.visitor_id = v.visitor_id) < 5 THEN 1 ELSE 0 END) AS segment_candidates
FROM pendo__visitor v