-- Execute once before S17; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c4" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture';
