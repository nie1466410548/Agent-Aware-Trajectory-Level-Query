-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.

-- S3
SELECT * FROM data LIMIT 10;

-- S4
SELECT COUNT(*) FROM data;

-- S5
SELECT DISTINCT "Floor Plan" FROM data ORDER BY "Floor Plan";

-- S6
SELECT DISTINCT Decoration FROM data ORDER BY Decoration;

-- S7
SELECT DISTINCT Floor FROM data ORDER BY Floor;

-- S8
SELECT DISTINCT Orientation FROM data ORDER BY Orientation;

-- BUILD C1 before S9
CREATE TEMP TABLE "reuse_015_c1" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT "Floor Plan", COUNT(*) AS cnt FROM data GROUP BY "Floor Plan" ORDER BY cnt DESC
) AS src;

-- S9
SELECT "Floor Plan", "cnt" FROM temp."reuse_015_c1" ORDER BY "__reuse_ordinal";

-- S10
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY cnt DESC;

-- S11
SELECT Decoration, COUNT(*) AS cnt FROM data GROUP BY Decoration ORDER BY cnt DESC;

-- S12
SELECT Orientation, COUNT(*) AS cnt FROM data GROUP BY Orientation ORDER BY cnt DESC;

-- BUILD C2 before S13
CREATE TEMP TABLE "reuse_015_c2" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY Floor
) AS src;

-- S13
SELECT "Floor", "cnt" FROM temp."reuse_015_c2" ORDER BY "__reuse_ordinal";

-- S14
SELECT Floor, COUNT(*) AS cnt FROM data WHERE Floor LIKE '%story%' OR Floor LIKE '%floors%' OR Floor LIKE '%floor building%' GROUP BY Floor ORDER BY cnt DESC;

-- S15
SELECT "Floor", "cnt" FROM temp."reuse_015_c2" ORDER BY "__reuse_ordinal";

-- S16
SELECT GROUP_CONCAT(Floor, ' | ') AS all_floors FROM (SELECT DISTINCT Floor FROM data ORDER BY Floor);

-- S17
SELECT "Floor Plan", "cnt" FROM temp."reuse_015_c1" ORDER BY "__reuse_ordinal";

-- S18
SELECT COUNT(*) AS total,
  SUM(CASE WHEN "Watch Count" > 0 THEN 1 ELSE 0 END) AS watch_gt0,
  SUM(CASE WHEN "Watch Count" = 0 THEN 1 ELSE 0 END) AS watch_eq0,
  SUM(CASE WHEN "Watch Count" > 50 THEN 1 ELSE 0 END) AS watch_gt50,
  SUM(CASE WHEN "Showings" > 0 THEN 1 ELSE 0 END) AS show_gt0,
  SUM(CASE WHEN "Showings" = 0 THEN 1 ELSE 0 END) AS show_eq0,
  SUM(CASE WHEN "Showings" > 10 THEN 1 ELSE 0 END) AS show_gt10,
  AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show,
  MAX("Watch Count") AS max_watch, MAX(Showings) AS max_show,
  MIN("Watch Count") AS min_watch, MIN(Showings) AS min_show
FROM data;

-- S19
SELECT "Watch Count", COUNT(*) AS cnt FROM data GROUP BY "Watch Count" ORDER BY "Watch Count" DESC LIMIT 20;

-- S20
SELECT DISTINCT Floor FROM data WHERE Floor LIKE '%th floor%' OR Floor LIKE '%st floor%' OR Floor LIKE '%nd floor%' OR Floor LIKE '%rd floor%' OR Floor LIKE 'Floor %';

-- S21
SELECT DISTINCT Floor FROM data WHERE Floor LIKE '%floors%' OR Floor LIKE '%story%' OR Floor LIKE '%Floors%';

-- S22
SELECT * FROM data;

-- S23
SELECT * FROM data;

-- S24
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
LIMIT 10;

-- S25
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
HAVING cnt >= 3
ORDER BY avg_watch_count DESC
LIMIT 10;

-- S26
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
LIMIT 25;

-- S27
SELECT "Floor Plan", Decoration, Floor, Orientation, "Watch Count", Showings
FROM data
WHERE "Floor Plan" = '4 bedrooms, 2 living rooms' AND Decoration = 'High-quality renovation' AND Floor = '18th floor' AND Orientation = 'North';

-- S28
SELECT Featured, COUNT(*) AS cnt, AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show FROM data GROUP BY Featured;

-- S29
SELECT "Date Published", COUNT(*) AS cnt, AVG("Watch Count") AS avg_watch, AVG(Showings) AS avg_show FROM data GROUP BY "Date Published" ORDER BY cnt DESC;

DROP TABLE temp."reuse_015_c2";
DROP TABLE temp."reuse_015_c1";
