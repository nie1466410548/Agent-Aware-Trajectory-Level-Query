WITH monthly AS (
  SELECT strftime('%Y-%m', "Date") AS month, SUM("Profit") AS total_profit
  FROM sheet1 WHERE "Destination" LIKE 'South China%'
  GROUP BY month
)
SELECT month, ROUND(total_profit,0) AS profit,
  ROUND(total_profit - LAG(total_profit) OVER (ORDER BY month),0) AS change_from_prev,
  ROUND((total_profit - LAG(total_profit) OVER (ORDER BY month))/LAG(total_profit) OVER (ORDER BY month)*100,1) AS pct_change
FROM monthly ORDER BY month