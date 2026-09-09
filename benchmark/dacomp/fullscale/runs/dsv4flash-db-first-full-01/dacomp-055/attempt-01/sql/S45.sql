SELECT 
  MIN(investment_priority_score) AS min_ips, MAX(investment_priority_score) AS max_ips, AVG(investment_priority_score) AS avg_ips
FROM (
  SELECT DISTINCT v.*, c_sales.total_sales_amount
  FROM customer360__customer_value_analysis v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
) base
WHERE product_adoption_rate IS NOT NULL 
  AND support_resolution_efficiency IS NOT NULL
  AND total_sales_amount IS NOT NULL
  AND acquisition_cost IS NOT NULL
  AND customer_lifetime_value IS NOT NULL