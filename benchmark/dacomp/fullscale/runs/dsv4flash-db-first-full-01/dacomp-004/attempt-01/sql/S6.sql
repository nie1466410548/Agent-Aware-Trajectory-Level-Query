WITH product_month AS (
  SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_amount,
         ROW_NUMBER() OVER (PARTITION BY "Sales Month" ORDER BY SUM("Sales Amount") DESC) AS rn
  FROM sheet1
  GROUP BY "Sales Month", "Product Code"
)
SELECT "Sales Month", "Product Code", ROUND(total_amount, 2) AS total_amount
FROM product_month
WHERE rn = 1
ORDER BY "Sales Month"