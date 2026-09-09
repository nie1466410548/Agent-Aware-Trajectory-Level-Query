-- Execute once before S65; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c14" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Discount" <> 'xxx' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL;
