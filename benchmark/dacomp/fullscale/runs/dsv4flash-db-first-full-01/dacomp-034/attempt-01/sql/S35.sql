-- Check fraction of SKU orders that are at a discount (SKU Cost Price > 0)
SELECT 'attachment_1' AS src,
       COUNT(*) AS total_orders,
       SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) AS discounted_orders,
       ROUND(100.0 * SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) / COUNT(*), 1) AS pct_discounted
FROM attachment_1
UNION ALL
SELECT 'attachment_2',
       COUNT(*),
       SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END),
       ROUND(100.0 * SUM(CASE WHEN "SKU Cost Price" > 0 THEN 1 ELSE 0 END) / COUNT(*), 1)
FROM attachment_2