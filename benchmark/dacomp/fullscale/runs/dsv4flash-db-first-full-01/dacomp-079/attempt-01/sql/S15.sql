SELECT
  CASE WHEN v.count_active_days > 60 AND fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'normal' END AS segment,
  ROUND(AVG(a.avg_nps_rating), 4) AS avg_account_nps,
  COUNT(*) AS n_users
FROM pendo__visitor v
LEFT JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
LEFT JOIN pendo__account a ON a.account_id = v.account_id
GROUP BY segment