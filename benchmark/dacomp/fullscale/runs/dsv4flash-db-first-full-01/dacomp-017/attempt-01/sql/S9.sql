SELECT "Product Category", 
       substr("Order Date",1,4) AS yr,
       SUM(profit) AS total_profit,
       SUM(Sales) AS total_sales,
       ROUND(SUM(profit)*1.0/SUM(Sales), 4) AS profit_margin
FROM order_information
GROUP BY "Product Category", yr
ORDER BY "Product Category", yr