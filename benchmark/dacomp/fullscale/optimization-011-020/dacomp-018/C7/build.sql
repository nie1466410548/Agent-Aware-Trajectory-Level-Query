-- Execute once before S5; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_018_c7" AS
SELECT "Customer ID" AS __g0, COUNT(*) AS __a0 FROM "customer_information"  GROUP BY "Customer ID";
