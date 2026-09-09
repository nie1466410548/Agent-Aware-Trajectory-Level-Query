-- Execute once before S16; retain this connection for subsequent reads.
CREATE TEMP TABLE "reuse_012_c2" AS
SELECT "Price (USD)" AS price, "Carat (diamond weight)" AS carat, "Cut (quality)" AS cut, "Color" AS color, "Clarity" AS clarity, CASE WHEN "Carat (diamond weight)" <= 0.5 THEN '<=0.5' WHEN "Carat (diamond weight)" <= 1.0 THEN '0.51-1.0' WHEN "Carat (diamond weight)" <= 1.5 THEN '1.01-1.5' ELSE '>1.5' END AS interval FROM sheet1;
