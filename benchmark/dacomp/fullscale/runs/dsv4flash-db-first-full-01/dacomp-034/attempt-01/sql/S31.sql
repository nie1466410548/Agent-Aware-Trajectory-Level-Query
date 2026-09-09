SELECT 
  a4."Level 1 Category Name" AS cat_name,
  a3.sale_count,
  ROUND(1.0 - a3.promotion_price / a3.pdj_price, 4) AS discount_depth,
  a3.promotion_price,
  a3.pdj_price,
  a3.cost_price,
  a3.allowance,
  a3.limit_count
FROM attachment_3 a3
JOIN attachment_4 a4 ON a3.sku_id = a4.sku_id
WHERE a3.promotion_type = 4 
  AND a3.state = 5 
  AND a3.pdj_price > 0
  AND a3.promotion_price > 0
  AND a3.sale_count > 0