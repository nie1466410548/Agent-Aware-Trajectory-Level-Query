WITH monthly AS (
  SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS total_profit
  FROM sheet1 WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT a.month, ROUND(a.total_profit,0) AS profit, 
  ROUND(a.total_profit - b.total_profit,0) AS change_from_prev,
  ROUND((a.total_profit - b.total_profit)/b.total_profit*100,1) AS pct_change
FROM monthly a
LEFT JOIN monthly b ON a.month = (SELECT MAX(month) FROM monthly m2 WHERE m2.month < a.month)
ORDER BY a.month