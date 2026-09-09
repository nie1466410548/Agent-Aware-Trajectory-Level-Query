-- Approved subset only. Other queries must run their original SQL.
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

-- S63
SELECT
  "Customer ID" AS "Customer ID",
  SUBSTRING("Order Date", 1, 4) AS "yr",
  profit AS "profit",
  Sales AS "Sales"
FROM temp."reuse_017_c4" AS order_information
WHERE
  "Product Category" = 'Home & Furniture';

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

DROP TABLE temp."reuse_017_c4";
