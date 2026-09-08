SELECT
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(SUM("List Price Revenue"),2) AS list_rev,
  ROUND(SUM("Logistics Value-Added Service Revenue"),2) AS vas_rev,
  ROUND(SUM("Discount Amount"),2) AS discount,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Freight Cost"),2) AS freight,
  ROUND(SUM("Warehousing Cost"),2) AS warehousing,
  ROUND(SUM("Other Operating Costs"),2) AS other_cost,
  ROUND(SUM("Total Logistics Cost"),2) AS cost,
  ROUND(SUM("Profit"),2) AS profit,
  ROUND(AVG("Profit Margin"),4) AS avg_margin
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month