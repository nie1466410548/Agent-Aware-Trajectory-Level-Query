SELECT o.Region, sp."Regional Manager",
       SUM(o.Sales) AS total_sales,
       SUM(o.profit) AS total_profit,
       ROUND(100.0 * SUM(o.profit) / SUM(o.Sales), 2) AS profit_margin_pct,
       COUNT(DISTINCT o."Order ID") AS n_orders,
       COUNT(*) AS n_rows
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager"
ORDER BY total_sales DESC