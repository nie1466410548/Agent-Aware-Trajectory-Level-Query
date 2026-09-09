SELECT o.Region, sp."Regional Manager",
       r."Return",
       COUNT(*) AS n_lines,
       COUNT(DISTINCT o."Order ID") AS n_orders
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
LEFT JOIN "return" r ON o."Order ID" = r."Order ID"
GROUP BY o.Region, sp."Regional Manager", r."Return"
ORDER BY o.Region, r."Return"