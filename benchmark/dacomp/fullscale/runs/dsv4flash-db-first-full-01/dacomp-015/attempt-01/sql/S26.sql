SELECT "Floor Plan", Decoration, Floor, Orientation, 
  COUNT(*) AS cnt,
  ROUND(AVG("Watch Count"),1) AS avg_watch,
  MAX("Watch Count") AS max_watch,
  SUM(CASE WHEN "Watch Count" >= 20 THEN 1 ELSE 0 END) AS n_ge20
FROM data
WHERE "Floor Plan" IS NOT NULL AND Decoration IS NOT NULL AND Floor IS NOT NULL AND Orientation IS NOT NULL
GROUP BY "Floor Plan", Decoration, Floor, Orientation
HAVING cnt >= 5
ORDER BY avg_watch DESC
LIMIT 25