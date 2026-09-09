SELECT "Floor Plan", Decoration, Floor, Orientation, 
  COUNT(*) AS cnt,
  AVG("Watch Count") AS avg_watch_count,
  SUM("Watch Count") AS total_watch_count,
  MAX("Watch Count") AS max_watch_count
FROM data
WHERE "Floor Plan" IS NOT NULL 
  AND Decoration IS NOT NULL 
  AND Floor IS NOT NULL 
  AND Orientation IS NOT NULL
GROUP BY "Floor Plan", Decoration, Floor, Orientation
HAVING cnt >= 5
ORDER BY avg_watch_count DESC
LIMIT 10