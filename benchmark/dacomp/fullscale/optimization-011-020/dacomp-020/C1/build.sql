-- Execute once before S17; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_020_c1" AS
SELECT * FROM sheet1;
