WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  CASE WHEN "Sales Quantity" <= 5 THEN 'Qty<=5' 
       WHEN "Sales Quantity" <= 10 THEN '6-10'
       WHEN "Sales Quantity" <= 20 THEN '11-20'
       WHEN "Sales Quantity" <= 40 THEN '21-40'
       ELSE '41+' END AS qty_band,
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100),2) AS avg_disc_rate,
  ROUND(AVG("Total Logistics Revenue"),2) AS avg_rev,
  ROUND(AVG("Total Logistics Cost"),2) AS avg_cost,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(AVG("Warehousing Cost"),2) AS avg_wh,
  ROUND(AVG("Other Operating Costs"),2) AS avg_other,
  ROUND(AVG("Profit"),2) AS avg_profit
FROM lm
GROUP BY qty_band, is_low
ORDER BY qty_band, is_low