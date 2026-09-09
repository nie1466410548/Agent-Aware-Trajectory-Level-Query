SELECT f.feature_id, f.feature_name, f.count_visitors AS feat_tbl_visitors,
       COUNT(vf.visitor_id) AS vf_rows, COUNT(DISTINCT vf.visitor_id) AS vf_distinct_visitors,
       SUM(vf.sum_clicks) AS vf_clicks
FROM pendo__feature f
LEFT JOIN pendo__visitor_feature vf ON vf.feature_id = f.feature_id
GROUP BY f.feature_id
ORDER BY f.count_visitors DESC
LIMIT 15