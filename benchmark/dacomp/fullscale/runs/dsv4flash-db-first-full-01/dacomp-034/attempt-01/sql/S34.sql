-- Check if attachment_1 and attachment_2 have overlapping data
SELECT COUNT(*) AS overlap FROM attachment_1 a1
JOIN attachment_2 a2 ON a1."Order ID" = a2."Order ID" AND a1.sku_id = a2.sku_id