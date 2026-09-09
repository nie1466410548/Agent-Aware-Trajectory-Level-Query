-- Execute once before S7; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_016_c1" AS
SELECT * FROM "sheet1" WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018;
