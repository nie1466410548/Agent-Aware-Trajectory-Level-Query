-- Execute once before S25; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_011_c1" AS
SELECT * FROM sheet1;
