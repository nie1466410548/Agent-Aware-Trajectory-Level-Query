-- Execute once before S22; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_015_c3" AS
SELECT * FROM data;
