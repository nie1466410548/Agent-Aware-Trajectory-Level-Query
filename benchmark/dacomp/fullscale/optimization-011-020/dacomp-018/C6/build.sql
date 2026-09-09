-- Execute once before S42; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c6" AS
SELECT "Customer ID", gender FROM customer_information GROUP BY "Customer ID";
