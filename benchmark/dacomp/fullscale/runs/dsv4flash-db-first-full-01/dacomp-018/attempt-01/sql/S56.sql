
WITH cust AS (SELECT "Customer ID", gender, age FROM customer_information GROUP BY "Customer ID"),
cust_orders AS (SELECT "Customer ID", SUM(profit) AS profit FROM order_information WHERE "Product Category" = 'Fashion' GROUP BY "Customer ID")
SELECT c.gender, c.age, co.profit FROM cust c JOIN cust_orders co ON c."Customer ID"=co."Customer ID"
