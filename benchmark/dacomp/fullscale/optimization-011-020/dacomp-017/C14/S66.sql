SELECT
  "Product" AS "Product",
  AVG(CAST("Discount" AS REAL)) AS "avg_discount",
  AVG(CAST("Quantity" AS REAL) * CAST("Discount" AS REAL)) AS "avg_qty_discount"
FROM temp."reuse_017_c14" AS order_information
WHERE
  "Product Category" = 'Home & Furniture'
  AND "Discount" <> 'xxx'
  AND "Quantity" <> 'abc'
  AND NOT "Quantity" IS NULL
GROUP BY
  "Product"
ORDER BY
  avg_qty_discount DESC;
