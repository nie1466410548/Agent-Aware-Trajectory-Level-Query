SELECT
  CASE
    WHEN "Destination" LIKE 'South China%' THEN 'South China'
    WHEN "Destination" LIKE 'North China%' THEN 'North China'
    WHEN "Destination" LIKE 'East China%' THEN 'East China'
    WHEN "Destination" LIKE 'Northeast%' THEN 'Northeast'
    WHEN "Destination" LIKE 'Northwest%' THEN 'Northwest'
    WHEN "Destination" LIKE 'Southwest%' THEN 'Southwest'
    ELSE 'Other' END AS region,
  strftime('%Y-%m', "Date") AS month,
  COUNT(*) AS orders,
  ROUND(SUM("Profit"),2) AS profit,
  ROUND(SUM("Total Logistics Revenue"),2) AS revenue,
  ROUND(SUM("Total Logistics Cost"),2) AS cost
FROM sheet1
GROUP BY region, month
ORDER BY region, month