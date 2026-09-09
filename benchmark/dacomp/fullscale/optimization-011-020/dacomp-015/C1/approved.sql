-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_015_c1" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT "Floor Plan", COUNT(*) AS cnt FROM data GROUP BY "Floor Plan" ORDER BY cnt DESC
) AS src;

-- S9
SELECT "Floor Plan", "cnt" FROM temp."reuse_015_c1" ORDER BY "__reuse_ordinal";

-- S17
SELECT "Floor Plan", "cnt" FROM temp."reuse_015_c1" ORDER BY "__reuse_ordinal";

DROP TABLE temp."reuse_015_c1";
