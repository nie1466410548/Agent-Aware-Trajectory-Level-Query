-- Execute once before S8; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c8" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Fashion';
