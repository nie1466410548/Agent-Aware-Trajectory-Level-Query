SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS sales
FROM "order" GROUP BY Category, yr ORDER BY Category, yr