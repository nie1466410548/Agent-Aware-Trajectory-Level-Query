
SELECT "Major Category Name", "Sales Month", 
       ROUND(SUM("Sales Amount"), 2) AS total_amount,
       SUM("Sales Quantity") AS total_qty,
       ROUND(SUM("Sales Amount") * 1.0 / NULLIF(SUM("Sales Quantity"), 0), 2) AS avg_unit_price
FROM sheet1
WHERE "Sales Quantity" > 0
GROUP BY "Major Category Name", "Sales Month"
ORDER BY "Major Category Name", "Sales Month"
