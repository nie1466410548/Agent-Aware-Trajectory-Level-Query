SELECT CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, COUNT(*) AS n_orders, COUNT(DISTINCT "Order ID") AS n_order_ids
FROM "order"
GROUP BY yr
ORDER BY yr