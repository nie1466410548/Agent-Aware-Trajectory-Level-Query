SELECT "Sales Month", "Product Code", ROUND(SUM("Sales Amount"), 2) AS total_amount, COUNT(*) AS transaction_count, COUNT(DISTINCT "Customer ID") AS customer_count
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Sales Month", "Product Code"
ORDER BY "Product Code", "Sales Month"