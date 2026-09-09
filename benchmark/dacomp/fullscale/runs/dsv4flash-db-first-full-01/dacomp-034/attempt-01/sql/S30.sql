-- Check the format of begin_time and create_dt
SELECT a3.begin_time, a3.end_time, a1.create_dt
FROM attachment_3 a3
JOIN attachment_1 a1 ON a3.sku_id = a1.sku_id
WHERE a3.promotion_type = 4 AND a3.state = 5
LIMIT 5