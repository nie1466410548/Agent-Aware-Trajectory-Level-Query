-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.
PRAGMA temp_store=MEMORY;
BEGIN;

-- S3
SELECT * FROM order_information LIMIT 20;

-- S4
SELECT * FROM product_browsing LIMIT 20;

-- BUILD C3 before S5
CREATE TEMP TABLE "reuse_017_c3" AS
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product Category" AS __g1, COUNT(*) AS __a0, SUM(profit) AS __a1, SUM(sales) AS __a2, SUM(CASE WHEN "Discount" = 'xxx' OR "Quantity" = 'abc' OR "Quantity" IS NULL THEN 1 ELSE 0 END) AS __a3, SUM(CASE WHEN profit < 0 THEN 1 ELSE 0 END) AS __a4, SUM(CASE WHEN profit < 0 THEN profit ELSE 0 END) AS __a5, MAX("Order Date") AS __a6, MIN("Order Date") AS __a7 FROM "order_information"  GROUP BY SUBSTRING("Order Date", 1, 4), "Product Category";

-- S5
SELECT
  SUM(__a0) AS "n"
FROM temp."reuse_017_c3";

-- S6
SELECT COUNT(*) AS n FROM product_browsing;

-- S7
SELECT DISTINCT "Product Category" FROM order_information;

-- S8
SELECT
  __g0 AS "yr",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c3"
GROUP BY
  __g0;

-- S9
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a1) AS "total_profit",
  SUM(__a2) AS "total_sales",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 4) AS "profit_margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S10
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 6) AS "pm"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S11
SELECT DISTINCT "Discount" FROM order_information ORDER BY "Discount";

-- S12
SELECT DISTINCT "Quantity" FROM order_information ORDER BY "Quantity";

-- S13
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a3) AS "bad_rows",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S14
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a4) AS "neg_rows",
  SUM(__a0) AS "n",
  SUM(__a5) AS "neg_profit"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S15
SELECT MIN(profit), MAX(profit), MIN(Sales), MAX(Sales) FROM order_information;

-- S16
SELECT "Order ID", "Product Category", "Product", Sales, "Discount", profit, profit*1.0/Sales AS order_margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Discount" = 'xxx'
LIMIT 20;

-- BUILD C4 before S17
CREATE TEMP TABLE "reuse_017_c4" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture';

-- S17
SELECT
  "Discount" AS "Discount",
  COUNT(*) AS "n",
  ROUND(AVG(profit * 1.0 / Sales), 4) AS "avg_margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Discount"
ORDER BY
  "Discount";

-- S18
SELECT
  "Shipping Method" AS "Shipping Method",
  COUNT(*) AS "n",
  SUM(profit) AS "total_profit",
  SUM(Sales) AS "total_sales",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Shipping Method"
ORDER BY
  "Shipping Method";

-- S19
SELECT
  "Discount" AS "Discount",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  COUNT(*) AS "n",
  AVG(profit * 1.0 / Sales) AS "avg_margin",
  AVG(profit) AS "avg_profit",
  AVG(Sales) AS "avg_sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Discount",
  yr
ORDER BY
  "Discount",
  yr;

-- S20
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Discount" AS "Discount",
  COUNT(*) AS "n",
  ROUND(SUM(profit), 1) AS "total_profit",
  ROUND(SUM(Sales), 1) AS "total_sales",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 6) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Discount"
ORDER BY
  yr,
  "Discount";

-- S21
SELECT
  "Product" AS "Product",
  COUNT(*) AS "n",
  SUM(Sales) AS "total_sales",
  SUM(profit) AS "total_profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 6) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product"
ORDER BY
  margin;

-- S22
SELECT DISTINCT
  "Product" AS "Product"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

-- S23
SELECT
  "Product" AS "Product",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  COUNT(*) AS "n",
  ROUND(SUM(Sales), 0) AS "total_sales",
  ROUND(SUM(profit), 1) AS "total_profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product",
  yr
ORDER BY
  "Product",
  yr;

-- S24
SELECT * FROM (
  SELECT "Product", substr("Order Date",1,4) AS yr,
         COUNT(*) AS n,
         ROUND(SUM(Sales),0) AS total_sales,
         ROUND(SUM(profit),1) AS total_profit,
         ROUND(SUM(profit)*1.0/SUM(Sales),6) AS margin
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Product", yr
  ORDER BY "Product", yr
) AS sub;

-- S25
SELECT yr, "Product", "Discount", COUNT(*) AS n, SUM(Sales) AS sales
FROM (
  SELECT substr("Order Date",1,4) AS yr, "Product", "Discount", Sales
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
) t
GROUP BY yr, "Product", "Discount"
ORDER BY yr, "Product", "Discount";

-- S26
SELECT "Product", substr("Order Date",1,4) AS yr,
       SUM(Sales) AS sales,
       SUM(Sales)*1.0 / SUM(SUM(Sales)) OVER (PARTITION BY substr("Order Date",1,4)) AS sales_share
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
GROUP BY "Product", yr
ORDER BY yr, sales_share DESC;

-- BUILD C6 before S27
CREATE TEMP TABLE "reuse_017_c6" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds';

-- S27
SELECT * FROM temp."reuse_017_c6" AS order_information WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Beds' LIMIT 10;

-- S28
SELECT
  profit AS "profit",
  Sales AS "Sales",
  "Discount" AS "Discount",
  profit * 1.0 / Sales AS "margin",
  Sales - profit AS "cost",
  "Quantity" AS "Quantity",
  "Shipping Cost" AS "Shipping Cost"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
LIMIT 20;

-- S29
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Discount" AS "Discount",
  COUNT(*) AS "n"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Discount"
ORDER BY
  yr,
  "Discount";

-- S30
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

-- S31
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Order Priority" AS "Order Priority",
  COUNT(*) AS "n"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  yr,
  "Order Priority"
ORDER BY
  yr,
  "Order Priority";

-- S32
SELECT
  "Quantity" AS "Quantity",
  "Discount" AS "Discount",
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  "Quantity",
  "Discount"
ORDER BY
  "Quantity",
  "Discount";

-- S33
SELECT DISTINCT
  Sales AS "Sales"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds';

-- S34
SELECT
  "Quantity" AS "Quantity",
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  "Quantity"
ORDER BY
  "Quantity";

-- S35
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

-- BUILD C8 before S36
CREATE TEMP TABLE "reuse_017_c8" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas';

-- S36
SELECT DISTINCT
  Sales AS "Sales"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas';

-- S37
SELECT
  "Quantity" AS "Quantity",
  COUNT(*) AS "n",
  SUM(profit) AS "profit",
  SUM(Sales) AS "sales",
  ROUND(SUM(profit) * 1.0 / SUM(Sales), 4) AS "margin"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY
  "Quantity"
ORDER BY
  "Quantity";

-- S38
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c6" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Beds'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

-- S39
SELECT
  SUBSTRING("Order Date", 1, 4) AS "yr",
  "Quantity" AS "Quantity",
  COUNT(*) AS "n"
FROM temp."reuse_017_c8" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Umbrellas'
GROUP BY
  yr,
  "Quantity"
ORDER BY
  yr,
  "Quantity";

-- S40
SELECT pb."Product Category", pb."Product", 
       AVG(pb."Browsing Time (minutes)") AS avg_browsing,
       AVG(pb."like") AS avg_like,
       AVG(pb."share") AS avg_share,
       AVG(pb."Add to Cart") AS avg_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Product"
ORDER BY avg_browsing DESC;

-- S41
SELECT pb."Product Category", pb."Product",
       COUNT(*) AS n,
       SUM(pb."like") AS total_likes,
       SUM(pb."share") AS total_shares,
       SUM(pb."Add to Cart") AS total_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Product"
ORDER BY n DESC;

-- S42
SELECT
  MAX(__a6) AS "max_date",
  MIN(__a7) AS "min_date"
FROM temp."reuse_017_c3";

-- S43
SELECT
  COUNT(DISTINCT "Customer ID") AS "n_customers"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

-- S44
SELECT
  COUNT(DISTINCT "Order ID") AS "n_orders"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

-- S45
WITH base AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary_profit,
         SUM(Sales) AS monetary_sales,
         COUNT(*) AS n_rows,
         SUM("Quantity" * 1.0) AS total_qty
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Customer ID"
)
SELECT "Customer ID", last_order, frequency, ROUND(monetary_profit,1) AS m_profit,
       monetary_sales, n_rows, ROUND(total_qty,1) AS total_qty,
       ROUND((julianday('2024-12-31') - julianday(last_order)),0) AS recency_days
FROM base
ORDER BY recency_days ASC
LIMIT 15;

-- S46
WITH base AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary_profit,
         SUM(Sales) AS monetary_sales,
         COUNT(*) AS n_rows,
         SUM(CAST("Quantity" AS REAL)) AS total_qty
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
    AND "Quantity" != 'abc'
    AND "Quantity" IS NOT NULL
  GROUP BY "Customer ID"
)
SELECT "Customer ID",
       ROUND((julianday('2024-12-31') - julianday(last_order)),0) AS recency,
       frequency,
       ROUND(monetary_profit, 1) AS monetary,
       ROUND(monetary_sales, 0) AS sales,
       ROUND(total_qty, 1) AS total_qty
FROM base
ORDER BY "Customer ID";

-- S47
WITH rfm AS (
  SELECT "Customer ID",
         MAX("Order Date") AS last_order,
         COUNT(DISTINCT "Order ID") AS frequency,
         SUM(profit) AS monetary
  FROM order_information
  WHERE "Product Category" = 'Home & Furniture'
  GROUP BY "Customer ID"
),
scored AS (
  SELECT "Customer ID",
         NTILE(4) OVER (ORDER BY julianday('2024-12-31') - julianday(last_order) DESC) AS R,
         NTILE(4) OVER (ORDER BY frequency ASC) AS F,
         NTILE(4) OVER (ORDER BY monetary ASC) AS M
  FROM rfm
)
SELECT CASE WHEN R+F+M >= 10 THEN 'Top Tier'
            WHEN R+F+M >= 7 THEN 'Mid Tier'
            WHEN R+F+M >= 4 THEN 'Low Tier'
            ELSE 'Bottom Tier' END AS segment,
       COUNT(*) AS n_customers
FROM scored
GROUP BY segment
ORDER BY n_customers DESC;

-- S48
SELECT "Customer ID", substr("Order Date",1,4) AS yr, 
       "Order ID", "Quantity", "Product", Sales, profit,
       profit * 1.0 / Sales AS margin
FROM order_information
WHERE "Product Category" = 'Home & Furniture'
  AND "Quantity" != 'abc'
  AND "Quantity" IS NOT NULL;

-- S49
SELECT "Product Category", "Product", Sales, profit, "Quantity"
FROM order_information
WHERE "Quantity" != 'abc' AND "Quantity" IS NOT NULL;

-- BUILD C1 before S50
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

-- BUILD C12 before S53
CREATE TEMP TABLE "reuse_017_c12" AS
SELECT * FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers';

-- S53
SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit",
  "Discount" AS "Discount",
  profit * 1.0 / Sales AS "margin"
FROM temp."reuse_017_c12" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers'
ORDER BY
  "Quantity",
  Sales
LIMIT 30;

-- S54
SELECT "Product", "Quantity", Sales, profit, profit*1.0/Sales AS margin
FROM order_information
WHERE "Product Category"='Home & Furniture' AND "Product"='Towels'
ORDER BY "Quantity", Sales
LIMIT 30;

-- S55
SELECT
  "Product" AS "Product",
  "Quantity" AS "Quantity",
  Sales AS "Sales",
  profit AS "profit",
  "Discount" AS "Discount",
  profit * 1.0 / Sales AS "margin"
FROM temp."reuse_017_c12" AS order_information
WHERE
  "Product Category" = 'Home & Furniture' AND "Product" = 'Sofa Covers'
ORDER BY
  "Quantity",
  "Discount";

-- S56
SELECT "Product", "Quantity", Sales, profit, "Discount", "Shipping Cost"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx';

-- S57
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  SUM(__a1) * 1.0 / SUM(__a2) AS "margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S58
SELECT
  "Product" AS "Product",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  SUM(profit) * 1.0 / SUM(Sales) AS "margin"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product",
  yr
ORDER BY
  "Product",
  yr;

-- BUILD C2 before S59
CREATE TEMP TABLE "reuse_017_c2" AS
SELECT "Customer ID", substr("Order Date",1,4) AS yr, "Quantity"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL;

-- S59
SELECT "Customer ID", "yr", "Quantity" FROM temp."reuse_017_c2";

-- S60
SELECT profit, Sales, "Quantity", "Discount"
FROM order_information
WHERE "Product Category" = 'Home & Furniture' AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx'
LIMIT 5000;

-- S61
SELECT
  "Product" AS "Product",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  SUM(Sales) AS "sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Product",
  yr
ORDER BY
  yr,
  sales DESC;

-- S62
SELECT "Customer ID", "yr", "Quantity" FROM temp."reuse_017_c2";

-- S63
SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  profit AS "profit",
  Sales AS "Sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

-- S64
SELECT pb."Customer ID", pb."Product Category", 
       AVG(pb."Browsing Time (minutes)") AS avg_browsing,
       AVG(pb."like") AS avg_like,
       AVG(pb."share") AS avg_share,
       AVG(pb."Add to Cart") AS avg_add_to_cart
FROM product_browsing pb
WHERE pb."Product Category" = 'Home & Furniture'
GROUP BY pb."Customer ID";

-- BUILD C15 before S65
CREATE TEMP TABLE "reuse_017_c15" AS
SELECT SUBSTRING("Order Date", 1, 4) AS __g0, "Product" AS __g1, SUM(CAST("Discount" AS REAL)) AS __a0_sum, COUNT(CAST("Discount" AS REAL)) AS __a0_n, SUM(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS __a1_sum, COUNT(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS __a1_n FROM "order_information" WHERE "Product Category" = 'Home & Furniture' AND "Discount" <> 'xxx' AND "Quantity" <> 'abc' AND NOT "Quantity" IS NULL GROUP BY SUBSTRING("Order Date", 1, 4), "Product";

-- S65
SELECT
  __g0 AS "yr",
  (
    1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)
  ) AS "avg_discount",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_qty_discount"
FROM temp."reuse_017_c15"
GROUP BY
  __g0
ORDER BY
  yr;

-- S66
SELECT
  __g1 AS "Product",
  (
    1.0 * SUM(__a0_sum) / NULLIF(SUM(__a0_n), 0)
  ) AS "avg_discount",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_qty_discount"
FROM temp."reuse_017_c15"
GROUP BY
  __g1
ORDER BY
  avg_qty_discount DESC;

-- S67
SELECT "Product", "Quantity", "Discount", Sales, profit
FROM order_information
WHERE "Product Category" = 'Home & Furniture' 
  AND "Quantity" != 'abc' AND "Quantity" IS NOT NULL AND "Discount" != 'xxx';

-- S68
SELECT
  __g1 AS "Product Category",
  __g0 AS "yr",
  ROUND(SUM(__a1) * 1.0 / SUM(__a2), 4) AS "margin"
FROM temp."reuse_017_c3"
GROUP BY
  __g1,
  __g0
ORDER BY
  __g1,
  yr;

-- S69
SELECT
  "Customer ID" AS "Customer ID",
  SUM(profit) AS "profit",
  SUM(Sales) AS "sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
GROUP BY
  "Customer ID";

-- S70
SELECT
  COUNT(*) AS "n",
  SUM(Sales) AS "sales",
  SUM(profit) AS "profit"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

-- S71
SELECT
  COUNT(DISTINCT "Order ID") AS "distinct_orders",
  COUNT(*) AS "rows_count"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

DROP TABLE temp."reuse_017_c3";
DROP TABLE temp."reuse_017_c4";
DROP TABLE temp."reuse_017_c6";
DROP TABLE temp."reuse_017_c1";
DROP TABLE temp."reuse_017_c8";
DROP TABLE temp."reuse_017_c2";
DROP TABLE temp."reuse_017_c15";
DROP TABLE temp."reuse_017_c12";
COMMIT;
