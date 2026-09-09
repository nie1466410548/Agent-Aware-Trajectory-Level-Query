SELECT Category, CAST(strftime('%Y', "Order Date") AS INTEGER) AS yr, SUM(Sales) AS total_sales, SUM(Quantity) AS total_qty, SUM(profit) AS total_profit
FROM "order"
WHERE strftime('%Y', "Order Date") BETWEEN '2015' AND '2018'
GROUP BY Category, yr
ORDER BY Category, yr