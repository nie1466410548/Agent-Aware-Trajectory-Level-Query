SELECT strftime('%m',"Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(SUM("Discount Amount"),0) AS discount,
  ROUND(SUM("Profit"),0) AS profit,
  ROUND(AVG("Profit Margin"),3) AS avg_margin,
  ROUND(SUM("Profit")/SUM("Sales Quantity"),2) AS profit_per_unit
FROM sheet1 
WHERE "Destination" LIKE 'South China%' AND "Consigned Product" = 'Kitchen Appliances'
GROUP BY month ORDER BY month