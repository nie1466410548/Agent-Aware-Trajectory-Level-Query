WITH order_returns AS (
  SELECT DISTINCT o."Order ID", o.Region, sp."Regional Manager",
         CASE WHEN r."Return" = 'Yes' THEN 1 ELSE 0 END AS is_returned
  FROM "order" o
  LEFT JOIN salesperson sp ON o.Region = sp.Region
  LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
)
SELECT Region, "Regional Manager",
       COUNT(DISTINCT "Order ID") AS total_orders,
       SUM(is_returned) AS returned_orders,
       ROUND(100.0 * SUM(is_returned) / COUNT(DISTINCT "Order ID"), 2) AS return_rate_pct
FROM order_returns
GROUP BY Region, "Regional Manager"
ORDER BY return_rate_pct DESC