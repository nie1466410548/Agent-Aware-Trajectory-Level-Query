-- Execute once before S13; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_015_c2" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT Floor, COUNT(*) AS cnt FROM data GROUP BY Floor ORDER BY Floor
) AS src;
