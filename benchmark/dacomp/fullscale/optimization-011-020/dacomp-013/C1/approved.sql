-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_013_c1" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status"
) AS src;

-- S10
SELECT "Task Type", "Task Status", "cnt" FROM temp."reuse_013_c1" ORDER BY "__reuse_ordinal";

-- S11
SELECT "Task Type", "Task Status", "cnt" FROM temp."reuse_013_c1" ORDER BY "__reuse_ordinal";

DROP TABLE temp."reuse_013_c1";
