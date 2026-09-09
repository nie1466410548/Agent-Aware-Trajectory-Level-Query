SELECT 
  "Consigned Product",
  strftime('%Y-%m', "Date") AS month,
  SUM("Profit") AS total_profit,
  COUNT(*) AS order_count,
  SUM("Sales Quantity") AS total_qty,
  SUM("Total Logistics Revenue") AS total_revenue,
  SUM("Total Logistics Cost") AS total_cost
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY "Consigned Product", month
ORDER BY "Consigned Product", month