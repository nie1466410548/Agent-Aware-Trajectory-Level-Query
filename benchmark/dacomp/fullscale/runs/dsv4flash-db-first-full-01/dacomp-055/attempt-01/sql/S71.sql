
SELECT email, MAX(total_sales_amount) AS total_sales_amount
FROM customer360__customer
WHERE total_sales_amount IS NOT NULL AND email IS NOT NULL
GROUP BY email
