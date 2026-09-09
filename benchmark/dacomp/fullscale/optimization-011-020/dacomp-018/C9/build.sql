-- Execute once before S9; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c9" AS
SELECT * FROM "product_browsing" WHERE "Product Category" = 'Fashion';
