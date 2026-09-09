-- Execute once before S9; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_015_c1" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT "Floor Plan", COUNT(*) AS cnt FROM data GROUP BY "Floor Plan" ORDER BY cnt DESC
) AS src;
