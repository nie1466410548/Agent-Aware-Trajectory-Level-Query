SELECT o.Region, sp."Regional Manager", o.Category,
       SUM(o.Sales) AS total_sales,
       ROUND(100.0 * SUM(o.Sales) / SUM(SUM(o.Sales)) OVER (PARTITION BY o.Region), 2) AS pct_of_region_sales
FROM "order" o
LEFT JOIN salesperson sp ON o.Region = sp.Region
GROUP BY o.Region, sp."Regional Manager", o.Category
ORDER BY o.Region, total_sales DESC