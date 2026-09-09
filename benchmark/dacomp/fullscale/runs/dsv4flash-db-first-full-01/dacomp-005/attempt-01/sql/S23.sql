WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  "Logistics Unit Price",
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_rev,
  ROUND(AVG("Freight Cost"), 2) AS avg_freight,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue",0) * 100), 2) AS avg_disc
FROM lm
GROUP BY "Logistics Unit Price", is_low
ORDER BY "Logistics Unit Price", is_low
LIMIT 40