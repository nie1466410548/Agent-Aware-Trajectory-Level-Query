WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
  WHERE "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1)
)
SELECT 
  "Sales Quantity",
  COUNT(*) AS n,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc_rate,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Total Logistics Cost"), 2) AS avg_cost,
  ROUND(AVG("Freight Cost"), 2) AS avg_freight,
  ROUND(AVG("Warehousing Cost"), 2) AS avg_wh,
  ROUND(AVG("Profit"), 2) AS avg_profit,
  ROUND(SUM("Profit"), 2) AS total_profit
FROM lm
GROUP BY "Sales Quantity"
ORDER BY "Sales Quantity"