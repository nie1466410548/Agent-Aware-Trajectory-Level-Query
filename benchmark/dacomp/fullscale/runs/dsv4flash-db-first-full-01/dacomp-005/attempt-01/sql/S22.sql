WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  ROUND(AVG("Freight Cost"), 2) AS lm_freight,
  ROUND(AVG("Warehousing Cost"), 2) AS lm_warehousing,
  ROUND(AVG("Other Operating Costs"), 2) AS lm_other,
  ROUND(AVG("Logistics Unit Price"), 2) AS lm_unit_price,
  ROUND(AVG("Logistics Value-Added Service Revenue"), 2) AS lm_vas
FROM lm
WHERE is_low = 1