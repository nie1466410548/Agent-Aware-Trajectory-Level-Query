-- Execute once before S53; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_017_c12" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers';
