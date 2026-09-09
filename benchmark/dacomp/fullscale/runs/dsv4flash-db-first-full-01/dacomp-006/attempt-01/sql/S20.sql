WITH monthly AS (
  SELECT 
    substr("Destination", 13, instr(substr("Destination", 13), '-') - 1) AS province,
    strftime('%Y-%m', "Date") AS month,
    SUM("Profit") AS total_profit,
    SUM("Sales Quantity") AS qty,
    COUNT(*) AS orders
  FROM sheet1
  WHERE "Destination" LIKE 'South China%'
  GROUP BY province, month
)
SELECT province,
  COUNT(*) AS months,
  ROUND(AVG(total_profit),0) AS mean_profit,
  ROUND(MIN(total_profit),0) AS min_profit,
  ROUND(MAX(total_profit),0) AS max_profit,
  ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit)),0) AS sd_profit,
  ROUND(SQRT(AVG(total_profit*total_profit)-AVG(total_profit)*AVG(total_profit))/AVG(total_profit)*100,1) AS cv_pct,
  ROUND(SUM(total_profit),0) AS annual_profit
FROM monthly
GROUP BY province
ORDER BY cv_pct DESC