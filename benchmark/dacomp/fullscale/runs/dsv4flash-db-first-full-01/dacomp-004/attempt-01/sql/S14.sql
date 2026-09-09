
SELECT "Sales Month" AS month, "Product Code" AS product, SUM("Sales Amount") AS sales_amount
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY product, month
