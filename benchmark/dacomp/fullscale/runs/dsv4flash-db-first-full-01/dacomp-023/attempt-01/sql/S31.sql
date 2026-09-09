SELECT o.Region, sp."Regional Manager",
       ROUND(SUM(o.Sales) / COUNT(DISTINCT o."Order ID"), 2) AS avg_sales_per_order,
       ROUND(SUM(o.profit) / COUNT(DISTINCT o."Order ID"), 2) AS avg_profit_per_order,
       ROUND(SUM(o.profit) / SUM(o.Sales) * 100, 2) AS profit_margin_pct,
       COUNT(DISTINCT o."Order ID") AS n_orders,
       ROUND(SUM(o.Sales) / COUNT(*), 2) AS avg_sales_per_line
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager"
ORDER BY avg_sales_per_order DESC