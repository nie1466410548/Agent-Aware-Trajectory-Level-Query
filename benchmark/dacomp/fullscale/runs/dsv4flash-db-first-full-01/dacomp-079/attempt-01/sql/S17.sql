SELECT COUNT(*) AS no_feature_visitors
FROM pendo__visitor v
WHERE NOT EXISTS (SELECT 1 FROM pendo__visitor_feature vf WHERE vf.visitor_id = v.visitor_id)