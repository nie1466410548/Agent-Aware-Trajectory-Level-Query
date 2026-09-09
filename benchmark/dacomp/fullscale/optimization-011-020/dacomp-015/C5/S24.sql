SELECT
  "Floor Plan" AS "Floor Plan",
  Decoration AS "Decoration",
  Floor AS "Floor",
  Orientation AS "Orientation",
  COUNT(*) AS "cnt",
  AVG("Watch Count") AS "avg_watch_count",
  SUM("Watch Count") AS "total_watch_count",
  MAX("Watch Count") AS "max_watch_count"
FROM temp."reuse_015_c5" AS data
WHERE
  NOT "Floor Plan" IS NULL
  AND NOT Decoration IS NULL
  AND NOT Floor IS NULL
  AND NOT Orientation IS NULL
GROUP BY
  "Floor Plan",
  Decoration,
  Floor,
  Orientation
HAVING
  cnt >= 5
ORDER BY
  avg_watch_count DESC
LIMIT 10;
