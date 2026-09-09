SELECT CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr,
       SUM(Sales) AS total_sales,
       SUM(profit) AS total_profit,
       ROUND(100.0 * SUM(profit) / SUM(Sales), 2) AS margin_pct
FROM "order"
GROUP BY yr ORDER BY yr