SELECT 
  a4."Level 1 Category Name" AS cat_name,
  a4."Level 1 Category ID" AS cat_id,
  COUNT(*) AS n_promos,
  SUM(a3.sale_count) AS total_sales,
  ROUND(AVG(1.0 - a3.promotion_price / a3.pdj_price), 4) AS avg_discount_depth,
  ROUND(AVG(a3.sale_count), 2) AS avg_sales_per_promo
FROM attachment_3 a3
JOIN attachment_4 a4 ON a3.sku_id = a4.sku_id
WHERE a3.promotion_type = 4 
  AND a3.state = 5 
  AND a3.pdj_price > 0
  AND a3.promotion_price > 0
GROUP BY a4."Level 1 Category Name"
ORDER BY total_sales DESC