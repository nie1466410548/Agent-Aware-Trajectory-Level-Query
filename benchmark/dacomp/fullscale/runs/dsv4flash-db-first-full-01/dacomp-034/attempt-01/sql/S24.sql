SELECT COUNT(DISTINCT a3.sku_id) AS skus_in_promo,
       COUNT(DISTINCT CASE WHEN a1.sku_id IS NOT NULL THEN a3.sku_id END) AS skus_in_orders
FROM (SELECT DISTINCT sku_id FROM attachment_3 WHERE promotion_type = 4 AND state = 5) a3
LEFT JOIN (SELECT DISTINCT sku_id FROM attachment_1) a1 ON a3.sku_id = a1.sku_id