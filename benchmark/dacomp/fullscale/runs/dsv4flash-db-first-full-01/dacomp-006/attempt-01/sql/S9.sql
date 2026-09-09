SELECT 
  "Destination",
  strftime('%Y-%m', "Date") AS month,
  SUM("Profit") AS total_profit,
  COUNT(*) AS order_count,
  SUM("Sales Quantity") AS total_qty
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY "Destination", month
ORDER BY "Destination", month