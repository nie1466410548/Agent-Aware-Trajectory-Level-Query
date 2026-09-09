SELECT 
  MIN(customer_lifetime_value) AS min_clv,
  MAX(customer_lifetime_value) AS max_clv,
  AVG(customer_lifetime_value) AS avg_clv,
  MIN(acquisition_cost) AS min_ac,
  MAX(acquisition_cost) AS max_ac,
  AVG(acquisition_cost) AS avg_ac
FROM customer360__customer_value_analysis