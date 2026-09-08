SELECT
  strftime('%Y-%m', "Date") AS month,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(AVG("Sales Quantity"),1) AS avg_qty_per_order,
  ROUND(AVG("List Price Revenue"),2) AS avg_list_rev_per_order,
  ROUND(AVG("Discount Amount"),2) AS avg_discount,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(SUM("Discount Amount")/SUM("List Price Revenue")*100,3) AS discount_rate_pct,
  ROUND(SUM("Freight Cost")/SUM("Total Logistics Revenue")*100,3) AS freight_ratio_pct
FROM sheet1
WHERE "Destination" LIKE 'South China%'
GROUP BY month
ORDER BY month