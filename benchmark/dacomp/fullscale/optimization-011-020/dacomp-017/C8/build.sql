-- Execute once before S36; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c8" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas';
