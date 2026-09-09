WITH pm AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT dim, month, ROUND(p,0) AS profit, 
  ROUND(p - LAG(p) OVER (PARTITION BY dim ORDER BY month),0) AS chg
FROM pm ORDER BY dim, month