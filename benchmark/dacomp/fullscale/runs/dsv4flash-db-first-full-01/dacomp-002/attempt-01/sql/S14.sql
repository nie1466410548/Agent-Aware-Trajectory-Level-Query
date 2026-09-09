-- Monthly sales amount and quantity for top 5 major categories with growth rate
WITH monthly AS (
  SELECT 
    "Major Category Name",
    "Sales Month",
    ROUND(SUM("Sales Amount"), 2) AS monthly_amount,
    SUM("Sales Quantity") AS monthly_qty,
    COUNT(*) AS trans_count
  FROM sheet1
  GROUP BY "Major Category Name", "Sales Month"
),
with_growth AS (
  SELECT *,
    LAG(monthly_amount) OVER (PARTITION BY "Major Category Name" ORDER BY "Sales Month") AS prev_amount,
    ROUND((monthly_amount - LAG(monthly_amount) OVER (PARTITION BY "Major Category Name" ORDER BY "Sales Month")) * 100.0 / NULLIF(LAG(monthly_amount) OVER (PARTITION BY "Major Category Name" ORDER BY "Sales Month"), 0), 1) AS growth_pct
  FROM monthly
)
SELECT * FROM with_growth ORDER BY "Major Category Name", "Sales Month"