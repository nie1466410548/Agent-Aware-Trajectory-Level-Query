-- Approved subset only. Other queries must run their original SQL.
CREATE TEMP TABLE "reuse_017_c5" AS
SELECT "Discount" AS __g0, "Shipping Method" AS __g1, SUBSTRING("Order Date", 1, 4) AS __g2, "Product" AS __g3, "Quantity" AS __g4, "Order Priority" AS __g5, "Customer ID" AS __g6, COUNT(*) AS __a0, SUM(profit * 1.0 / sales) AS __a1_sum, COUNT(profit * 1.0 / sales) AS __a1_n, SUM(profit) AS __a2, SUM(sales) AS __a3, SUM(profit) AS __a4_sum, COUNT(profit) AS __a4_n, SUM(sales) AS __a5_sum, COUNT(sales) AS __a5_n FROM "order_information" WHERE "Product Category" = 'Home & Furniture' GROUP BY "Discount", "Shipping Method", SUBSTRING("Order Date", 1, 4), "Product", "Quantity", "Order Priority", "Customer ID";

-- S17
SELECT
  __g0 AS "Discount",
  SUM(__a0) AS "n",
  ROUND((
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ), 4) AS "avg_margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g0
ORDER BY
  __g0;

-- S18
SELECT
  __g1 AS "Shipping Method",
  SUM(__a0) AS "n",
  SUM(__a2) AS "total_profit",
  SUM(__a3) AS "total_sales",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 4) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g1
ORDER BY
  __g1;

-- S19
SELECT
  __g0 AS "Discount",
  __g2 AS "yr",
  SUM(__a0) AS "n",
  (
    1.0 * SUM(__a1_sum) / NULLIF(SUM(__a1_n), 0)
  ) AS "avg_margin",
  (
    1.0 * SUM(__a4_sum) / NULLIF(SUM(__a4_n), 0)
  ) AS "avg_profit",
  (
    1.0 * SUM(__a5_sum) / NULLIF(SUM(__a5_n), 0)
  ) AS "avg_sales"
FROM temp."reuse_017_c5"
GROUP BY
  __g0,
  __g2
ORDER BY
  __g0,
  yr;

-- S20
SELECT
  __g2 AS "yr",
  __g0 AS "Discount",
  SUM(__a0) AS "n",
  ROUND(SUM(__a2), 1) AS "total_profit",
  ROUND(SUM(__a3), 1) AS "total_sales",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 6) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;

-- S21
SELECT
  __g3 AS "Product",
  SUM(__a0) AS "n",
  SUM(__a3) AS "total_sales",
  SUM(__a2) AS "total_profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 6) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g3
ORDER BY
  margin;

-- S23
SELECT
  __g3 AS "Product",
  __g2 AS "yr",
  SUM(__a0) AS "n",
  ROUND(SUM(__a3), 0) AS "total_sales",
  ROUND(SUM(__a2), 1) AS "total_profit",
  ROUND(SUM(__a2) * 1.0 / SUM(__a3), 4) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g3,
  __g2
ORDER BY
  __g3,
  yr;

-- S29
SELECT
  __g2 AS "yr",
  __g0 AS "Discount",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g0
ORDER BY
  yr,
  __g0;

-- S30
SELECT
  __g2 AS "yr",
  __g4 AS "Quantity",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g4
ORDER BY
  yr,
  __g4;

-- S31
SELECT
  __g2 AS "yr",
  __g5 AS "Order Priority",
  SUM(__a0) AS "n"
FROM temp."reuse_017_c5"
GROUP BY
  __g2,
  __g5
ORDER BY
  yr,
  __g5;

-- S58
SELECT
  __g3 AS "Product",
  __g2 AS "yr",
  SUM(__a2) * 1.0 / SUM(__a3) AS "margin"
FROM temp."reuse_017_c5"
GROUP BY
  __g3,
  __g2
ORDER BY
  __g3,
  yr;

-- S61
SELECT
  __g3 AS "Product",
  __g2 AS "yr",
  SUM(__a3) AS "sales"
FROM temp."reuse_017_c5"
GROUP BY
  __g3,
  __g2
ORDER BY
  yr,
  sales DESC;

DROP TABLE temp."reuse_017_c5";
