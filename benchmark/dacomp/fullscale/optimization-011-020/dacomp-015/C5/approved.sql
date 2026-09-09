-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_015_c5" AS
SELECT * FROM "data" WHERE NOT "Floor Plan" IS NULL AND NOT decoration IS NULL AND NOT floor IS NULL AND NOT orientation IS NULL;

-- S24
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

-- S25
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
  cnt >= 3
ORDER BY
  avg_watch_count DESC
LIMIT 10;

-- S26
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

DROP TABLE temp."reuse_015_c5";
