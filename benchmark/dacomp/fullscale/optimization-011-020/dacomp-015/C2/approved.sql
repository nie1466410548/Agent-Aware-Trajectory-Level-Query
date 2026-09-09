-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_015_c2" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY Floor
) AS src;

-- S13
SELECT "Floor", "cnt" FROM temp."reuse_015_c2" ORDER BY "__reuse_ordinal";

-- S15
SELECT "Floor", "cnt" FROM temp."reuse_015_c2" ORDER BY "__reuse_ordinal";

DROP TABLE temp."reuse_015_c2";
