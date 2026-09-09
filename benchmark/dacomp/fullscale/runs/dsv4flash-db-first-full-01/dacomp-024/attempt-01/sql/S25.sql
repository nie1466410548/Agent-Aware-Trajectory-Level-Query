SELECT Region, COUNT(DISTINCT State) AS states, COUNT(DISTINCT City) AS cities,
       COUNT(DISTINCT "Customer ID") AS total_customers_2015_17
FROM sheet1
WHERE substr("Order Date", -4, 4) IN ('2015','2016','2017')
GROUP BY Region ORDER BY total_customers_2015_17 DESC