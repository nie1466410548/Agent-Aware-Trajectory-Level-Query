SELECT
  "Floor Plan" AS "Floor Plan",
  Decoration AS "Decoration",
  Floor AS "Floor",
  Orientation AS "Orientation",
  COUNT(*) AS "cnt",
  ROUND(AVG("Watch Count"), 1) AS "avg_watch",
  MAX("Watch Count") AS "max_watch",
  SUM(CASE WHEN "Watch Count" >= 20 THEN 1 ELSE 0 END) AS "n_ge20"
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
  avg_watch DESC
LIMIT 25;
