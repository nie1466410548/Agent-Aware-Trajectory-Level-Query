SELECT
  COUNT(*) AS n_features,
  SUM(CASE WHEN count_visitors < 200 THEN 1 ELSE 0 END) AS n_below_200,
  SUM(CASE WHEN count_visitors BETWEEN 200 AND 1000 THEN 1 ELSE 0 END) AS n_200_1000,
  SUM(CASE WHEN count_visitors > 1000 THEN 1 ELSE 0 END) AS n_above_1000,
  MIN(count_visitors) AS min_v, MAX(count_visitors) AS max_v, AVG(count_visitors) AS avg_v
FROM pendo__feature