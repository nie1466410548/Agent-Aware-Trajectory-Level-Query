SELECT 
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS order_count,
  SUM("Profit") AS total_profit,
  SUM("Total Logistics Revenue") AS total_revenue,
  SUM("Total Logistics Cost") AS total_cost,
  AVG("Profit Margin") AS avg_profit_margin
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month