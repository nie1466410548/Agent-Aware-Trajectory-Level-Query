WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Freight Cost") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS freight_pct_of_rev,
  ROUND(AVG("Warehousing Cost") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS warehousing_pct_of_rev,
  ROUND(AVG("Other Operating Costs") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS other_op_pct_of_rev,
  ROUND(AVG("Total Logistics Cost") / NULLIF(AVG("Total Logistics Revenue"),0) * 100, 2) AS cost_pct_of_rev,
  ROUND(AVG("Total Logistics Revenue") / NULLIF(AVG("Sales Quantity"),0), 2) AS revenue_per_unit,
  ROUND(AVG("Total Logistics Cost") / NULLIF(AVG("Sales Quantity"),0), 2) AS cost_per_unit
FROM lm
GROUP BY is_low