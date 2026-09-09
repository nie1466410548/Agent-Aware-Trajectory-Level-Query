SELECT Region,
       COUNT(DISTINCT "Order ID") AS orders,
       COUNT(DISTINCT "Customer ID") AS customers,
       SUM(s2.Quantity) AS qty,
       SUM(s2.Quantity*s2."Sales per Unit") AS sales,
       SUM(s2.Quantity*s2."Profit per Unit") AS profit
FROM sheet1 s1 JOIN sheet2 s2 ON s1."Order ID"=s2."Order ID"
WHERE substr(s1."Order Date",-4,4) IN ('2015','2016','2017')
GROUP BY Region ORDER BY sales DESC