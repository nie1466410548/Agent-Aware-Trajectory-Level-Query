SELECT "Product Code", 
       ROUND(SUM("Sales Amount"), 2) AS total_sales_amount,
       COUNT(*) AS total_transactions,
       COUNT(DISTINCT "Customer ID") AS total_customers,
       ROUND(AVG("Sales Amount"), 2) AS avg_transaction_amount
FROM sheet1
WHERE "Product Code" IN ('DW-1001040125', 'DW-2316020016', 'DW-1203130446', 'DW-1518040045')
GROUP BY "Product Code"
ORDER BY "Product Code"