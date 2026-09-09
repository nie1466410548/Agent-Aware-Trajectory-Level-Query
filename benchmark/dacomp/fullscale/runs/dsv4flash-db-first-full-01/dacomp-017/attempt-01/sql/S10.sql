SELECT "Product Category",
       substr("Order Date",1,4) AS yr,
       ROUND(SUM(profit)*1.0/SUM(Sales),6) AS pm
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr