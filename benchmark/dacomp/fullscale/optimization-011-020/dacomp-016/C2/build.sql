-- Execute once before S8; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_016_c2" AS
SELECT * FROM "economic_indicator_data" WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018;
