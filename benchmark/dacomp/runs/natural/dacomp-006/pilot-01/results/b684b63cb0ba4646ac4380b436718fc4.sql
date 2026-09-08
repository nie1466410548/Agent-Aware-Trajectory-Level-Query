SELECT
  SUBSTR(SUBSTR("Destination", INSTR("Destination",'-')+1), 1,
         INSTR(SUBSTR("Destination", INSTR("Destination",'-')+1),'-')-1) AS province,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  SUM("Sales Quantity") AS qty,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Profit"),2) AS profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY province, month
ORDER BY province, month