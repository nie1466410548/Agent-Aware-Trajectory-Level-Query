SELECT 
  "Consigned Product" AS dim,
  ROUND(SUM(CASE WHEN strftime('%m',"Date")='01' THEN "Profit" ELSE 0 END),0) AS jan,
  ROUND(SUM(CASE WHEN strftime('%m',"Date")='02' THEN "Profit" ELSE 0 END),0) AS feb,
  ROUND(SUM(CASE WHEN strftime('%m',"Date")='02' THEN "Profit" ELSE 0 END) - SUM(CASE WHEN strftime('%m',"Date")='01' THEN "Profit" ELSE 0 END),0) AS change,
  ROUND(AVG("Profit"),0) AS avg_monthly
FROM sheet1 WHERE "Destination" LIKE 'South China%'
GROUP BY dim
ORDER BY ABS(change) DESC