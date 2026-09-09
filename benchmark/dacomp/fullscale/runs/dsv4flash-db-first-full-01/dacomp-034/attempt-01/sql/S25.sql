SELECT 
  promotion_type,
  ROUND(AVG(1.0 - promotion_price / pdj_price), 4) AS avg_discount_depth,
  ROUND(SUM(sale_count), 0) AS total_sales,
  COUNT(*) AS n_promos
FROM attachment_3 
WHERE promotion_type IS NOT NULL 
  AND state = 5
  AND pdj_price > 0
  AND promotion_price > 0
GROUP BY promotion_type