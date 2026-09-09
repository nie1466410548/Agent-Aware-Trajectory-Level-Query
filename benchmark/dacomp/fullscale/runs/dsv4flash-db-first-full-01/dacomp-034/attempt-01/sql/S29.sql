-- Check if we can find corresponding orders for promotion skus
-- How many promotions have orders in the same time period?
SELECT COUNT(*) AS n_matches
FROM attachment_3 a3
JOIN attachment_1 a1 
  ON a3.sku_id = a1.sku_id
  AND a1.create_dt >= a3.begin_time
  AND a1.create_dt <= a3.end_time
WHERE a3.promotion_type = 4 
  AND a3.state = 5
  AND a3.pdj_price > 0
  AND a3.sale_count > 0
  AND a3.sku_id IN (SELECT DISTINCT sku_id FROM attachment_1)