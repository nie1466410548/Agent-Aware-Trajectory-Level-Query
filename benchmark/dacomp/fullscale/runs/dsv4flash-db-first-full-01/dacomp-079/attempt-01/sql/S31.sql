-- NPS distributions for the two within-heavy segments
SELECT
  CASE WHEN fv.distinct_features < 5 THEN 'single_feature_heavy' ELSE 'multi_feature_heavy' END AS segment,
  ROUND(MIN(v.latest_nps_rating), 1) AS min_nps,
  ROUND(AVG(v.latest_nps_rating), 3) AS avg_nps,
  ROUND(MAX(v.latest_nps_rating), 1) AS max_nps,
  COUNT(*) AS n
FROM pendo__visitor v
JOIN (
  SELECT visitor_id, COUNT(DISTINCT feature_id) AS distinct_features
  FROM pendo__visitor_feature
  GROUP BY visitor_id
) fv ON fv.visitor_id = v.visitor_id
WHERE v.count_active_days > 60
GROUP BY segment