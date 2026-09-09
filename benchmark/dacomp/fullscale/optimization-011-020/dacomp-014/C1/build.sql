-- Execute once before S36; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_014_c1" AS
SELECT * FROM sheet1;
