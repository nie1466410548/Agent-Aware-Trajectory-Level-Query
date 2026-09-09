SELECT
  CASE WHEN count_visitors < 200 THEN '<200'
       WHEN count_visitors < 500 THEN '200-500'
       WHEN count_visitors < 1000 THEN '500-1000'
       ELSE '>=1000' END AS usage_band,
  COUNT(*) AS n_features
FROM pendo__feature
GROUP BY usage_band
ORDER BY MIN(count_visitors)