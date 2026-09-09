SELECT AVG(cnt) AS avg_features_per_visitor,
       MIN(cnt) AS min_features,
       MAX(cnt) AS max_features
FROM (SELECT visitor_id, COUNT(*) AS cnt FROM pendo__visitor_feature GROUP BY visitor_id)