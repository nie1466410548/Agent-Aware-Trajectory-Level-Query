
SELECT "Sales Month", COUNT(DISTINCT "Customer ID") AS customer_count, COUNT(*) AS trans_count
FROM sheet1
GROUP BY "Sales Month" ORDER BY "Sales Month"
