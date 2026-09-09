SELECT "Sales Month", "Product Code", SUM("Sales Amount") AS total_amount
FROM sheet1
GROUP BY "Sales Month", "Product Code"
ORDER BY "Sales Month", total_amount DESC