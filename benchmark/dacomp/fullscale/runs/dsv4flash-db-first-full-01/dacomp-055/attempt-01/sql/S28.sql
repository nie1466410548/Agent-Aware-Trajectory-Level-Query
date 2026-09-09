SELECT email, COUNT(*) AS cnt, COUNT(DISTINCT total_sales_amount) AS distinct_sales, MAX(total_sales_amount) AS max_sales, MIN(total_sales_amount) AS min_sales
FROM customer360__customer
WHERE email = 'muriel.davis@gmail.com'
GROUP BY email