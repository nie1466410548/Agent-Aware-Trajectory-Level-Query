SELECT s1.Region, s1.Segment, substr(s1."Order Date", -4, 4) AS year,
       COUNT(DISTINCT s1."Order ID") AS order_count,
       COUNT(DISTINCT s1."Customer ID") AS customer_count,
       SUM(s2.Quantity) AS total_quantity,
       SUM(s2.Quantity * s2."Sales per Unit") AS total_sales,
       SUM(s2.Quantity * s2."Profit per Unit") AS total_profit,
       AVG(s2.Discount) AS avg_discount,
       SUM(s2.Quantity * (s2."Sales per Unit" - s2."Profit per Unit")) AS total_cost
FROM sheet1 s1
JOIN sheet2 s2 ON s1."Order ID" = s2."Order ID"
WHERE substr(s1."Order Date", -4, 4) IN ('2015', '2016', '2017')
GROUP BY s1.Region, s1.Segment, year
ORDER BY Region, Segment, year