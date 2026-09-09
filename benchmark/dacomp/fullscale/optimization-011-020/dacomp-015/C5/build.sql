-- Execute once before S24; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_015_c5" AS
SELECT * FROM "data" WHERE NOT "Floor Plan" IS NULL AND NOT decoration IS NULL AND NOT floor IS NULL AND NOT orientation IS NULL;
