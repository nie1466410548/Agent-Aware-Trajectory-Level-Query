SELECT o.Region,
       ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS margin,
       COUNT(DISTINCT o."Order ID") AS total_orders
FROM "order" o GROUP BY o.Region