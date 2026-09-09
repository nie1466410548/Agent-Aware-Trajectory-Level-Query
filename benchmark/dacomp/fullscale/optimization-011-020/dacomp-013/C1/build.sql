-- Execute once before S10; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_013_c1" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT "Task Type", "Task Status", COUNT(*) AS cnt
FROM sheet1 GROUP BY "Task Type", "Task Status" ORDER BY "Task Type", "Task Status"
) AS src;
