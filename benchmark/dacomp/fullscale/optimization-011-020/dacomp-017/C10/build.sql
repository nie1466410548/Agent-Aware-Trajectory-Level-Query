-- Execute once before S40; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c10" AS
SELECT * FROM "product_browsing" WHERE "Product Category" = 'Home & Furniture';
