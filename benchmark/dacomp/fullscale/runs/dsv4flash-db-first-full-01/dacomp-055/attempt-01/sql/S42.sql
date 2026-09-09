SELECT 
  COUNT(*) AS total,
  SUM(CASE WHEN v.investment_priority_score IS NULL THEN 1 ELSE 0 END) AS null_ips,
  SUM(CASE WHEN v.product_adoption_rate IS NULL THEN 1 ELSE 0 END) AS null_par,
  SUM(CASE WHEN v.support_resolution_efficiency IS NULL THEN 1 ELSE 0 END) AS null_sre,
  SUM(CASE WHEN v.total_sales_amount IS NULL THEN 1 ELSE 0 END) AS null_sales,
  SUM(CASE WHEN v.acquisition_cost IS NULL THEN 1 ELSE 0 END) AS null_ac,
  SUM(CASE WHEN v.customer_lifetime_value IS NULL THEN 1 ELSE 0 END) AS null_clv
FROM (
  SELECT DISTINCT v.*, c_sales.total_sales_amount
  FROM customer360__customer_value_analysis v
  LEFT JOIN (
    SELECT email, MAX(total_sales_amount) AS total_sales_amount
    FROM customer360__customer
    WHERE total_sales_amount IS NOT NULL
    GROUP BY email
  ) c_sales ON v.primary_email = c_sales.email
) v