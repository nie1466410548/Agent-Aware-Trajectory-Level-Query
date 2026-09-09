SELECT o.Region, sp."Regional Manager", o."Order ID", SUM(o.Sales) AS order_sales
FROM "order" o LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, o."Order ID" ORDER BY o.Region, o."Order ID"