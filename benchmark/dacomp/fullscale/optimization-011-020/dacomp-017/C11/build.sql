-- Execute once before S48; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c11" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL;
