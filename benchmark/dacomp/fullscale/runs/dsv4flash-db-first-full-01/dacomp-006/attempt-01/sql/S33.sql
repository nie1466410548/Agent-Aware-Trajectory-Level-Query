SELECT strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),0) AS profit,
  ROUND(AVG("Profit"),0) AS avg_profit_per_order,
  ROUND(AVG("Sales Quantity"),1) AS avg_qty,
  ROUND(AVG("Profit Margin"),3) AS avg_margin,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price
FROM sheet1 WHERE "Destination" LIKE 'South China%'
GROUP BY month ORDER BY month