-- Execute once before S9; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_012_c1" AS
SELECT "Price (USD)" AS price, "Carat (diamond weight)" AS carat, CASE WHEN "Carat (diamond weight)" <= 0.5 THEN 'A: <=0.5 ct' WHEN "Carat (diamond weight)" <= 1.0 THEN 'B: 0.51-1.0 ct' WHEN "Carat (diamond weight)" <= 1.5 THEN 'C: 1.01-1.5 ct' ELSE 'D: >1.5 ct' END AS interval FROM sheet1;
