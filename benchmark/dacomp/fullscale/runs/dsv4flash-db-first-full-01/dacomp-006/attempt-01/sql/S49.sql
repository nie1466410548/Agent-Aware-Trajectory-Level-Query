WITH pm AS (
  SELECT "Consigned Product" AS dim, strftime('%Y-%m',"Date") AS month, SUM("Profit") AS p
  FROM sheet1 WHERE "Destination" LIKE 'South China%' GROUP BY 1,2
)
SELECT dim, 
  ROUND(AVG(p),0) AS mean_p,
  ROUND(MIN(p),0) AS min_p,
  ROUND(MAX(p),0) AS max_p,
  ROUND((MAX(p)-MIN(p))/AVG(p)*100,1) AS range_pct,
  ROUND(SQRT(AVG(p*p)-AVG(p)*AVG(p)),0) AS std_p,
  ROUND(SQRT(AVG(p*p)-AVG(p)*AVG(p))/AVG(p)*100,1) AS cv_pct
FROM pm GROUP BY dim ORDER BY cv_pct DESC