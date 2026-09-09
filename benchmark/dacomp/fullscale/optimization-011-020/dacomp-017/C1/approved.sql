-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c1" AS
SELECT substr("Order Date",1,4) AS yr, "Product", "Quantity",
       Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL;

-- S50
SELECT "yr", "Product", "Quantity", "Sales", "profit" FROM temp."reuse_017_c1";

-- S51
SELECT "yr", "Product", "Quantity", "Sales", "profit" FROM temp."reuse_017_c1";

-- S52
SELECT "yr", "Product", "Quantity", "Sales", "profit" FROM temp."reuse_017_c1";

DROP TABLE temp."reuse_017_c1";
