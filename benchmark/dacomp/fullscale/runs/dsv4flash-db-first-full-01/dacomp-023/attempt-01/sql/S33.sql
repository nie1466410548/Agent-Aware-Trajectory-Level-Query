SELECT o.Region, sp."Regional Manager",
       ROUND(AVG(o.Discount) * 100, 2) AS avg_discount_pct,
       ROUND(SUM(o.Quantity), 0) AS total_qty,
       ROUND(SUM(o.Sales) / SUM(o.Quantity), 2) AS avg_price_per_unit
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager"
ORDER BY avg_discount_pct DESC