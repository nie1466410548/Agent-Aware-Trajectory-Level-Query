WITH prod_month AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT month, 
  ROUND(p,0) AS kitchen_appl_profit,
  ROUND(p - AVG(p) OVER (PARTITION BY dim),0) AS deviation_from_mean
FROM prod_month
WHERE dim = 'Kitchen Appliances'
ORDER BY month