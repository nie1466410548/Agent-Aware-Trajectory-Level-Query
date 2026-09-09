SELECT 
  MIN(investment_priority_score) AS min_ips,
  MAX(investment_priority_score) AS max_ips,
  AVG(investment_priority_score) AS avg_ips,
  MIN(total_sales_amount) AS min_sales,
  MAX(total_sales_amount) AS max_sales,
  AVG(total_sales_amount) AS avg_sales,
  MIN(product_adoption_rate) AS min_par,
  MAX(product_adoption_rate) AS max_par,
  AVG(product_adoption_rate) AS avg_par,
  MIN(support_resolution_efficiency) AS min_sre,
  MAX(support_resolution_efficiency) AS max_sre,
  AVG(support_resolution_efficiency) AS avg_sre
FROM customer360__customer_value_analysis