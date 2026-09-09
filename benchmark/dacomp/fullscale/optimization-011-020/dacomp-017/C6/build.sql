-- Execute once before S27; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c6" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds';
