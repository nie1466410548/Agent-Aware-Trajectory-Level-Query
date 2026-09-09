-- Build the analytical dataset with distinct rows, joined sales data
SELECT COUNT(*) AS total_rows,
  MIN(investment_priority_score) AS min_ips,
  MAX(investment_priority_score) AS max_ips,
  MIN(product_adoption_rate) AS min_par,
  MAX(product_adoption_rate) AS max_par,
  MIN(support_resolution_efficiency) AS min_sre,
  MAX(support_resolution_efficiency) AS max_sre,
  MIN(total_sales_amount) AS min_sales,
  MAX(total_sales_amount) AS max_sales,
  MIN(acquisition_cost) AS min_ac,
  MAX(acquisition_cost) AS max_ac,
  MIN(customer_lifetime_value) AS min_clv,
  MAX(customer_lifetime_value) AS max_clv
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