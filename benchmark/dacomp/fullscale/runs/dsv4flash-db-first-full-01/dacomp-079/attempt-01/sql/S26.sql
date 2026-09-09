-- Concentration: share of clicks on the dominant feature per user
WITH user_feature AS (
  SELECT vf.visitor_id, fv.distinct_features,
    vf.feature_id, vf.sum_clicks
  FROM pendo__visitor_feature vf
  JOIN pendo__visitor v ON v.visitor_id = vf.visitor_id
  JOIN (SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
        FROM pendo__visitor_feature GROUP BY visitor_id) fv ON fv.visitor_id = v.visitor_id
  WHERE v.count_active_days > 60 AND fv.distinct_features < 5
),
user_totals AS (
  SELECT visitor_id, distinct_features, SUM(sum_clicks) AS total_clicks
  FROM user_feature GROUP BY visitor_id
),
user_max AS (
  SELECT visitor_id, MAX(sum_clicks) AS max_feature_clicks
  FROM user_feature GROUP BY visitor_id
)
SELECT
  uf.distinct_features,
  COUNT(DISTINCT uf.visitor_id) AS n_users,
  ROUND(AVG(um.max_feature_clicks * 1.0 / ut.total_clicks), 4) AS avg_dominant_share,
  ROUND(AVG(ut.total_clicks), 1) AS avg_total_clicks
FROM user_feature uf
JOIN user_totals ut ON ut.visitor_id = uf.visitor_id
JOIN user_max um ON um.visitor_id = uf.visitor_id
GROUP BY uf.distinct_features
ORDER BY uf.distinct_features