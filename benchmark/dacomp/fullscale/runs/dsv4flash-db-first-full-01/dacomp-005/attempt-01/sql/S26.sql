WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  ROUND(AVG("Discount Amount" / NULLIF("List Price Revenue", 0) * 100), 2) AS avg_discount_rate,
  ROUND(AVG("List Price Revenue"), 2) AS avg_list_price,
  ROUND(AVG("Total Logistics Revenue"), 2) AS avg_logistics_rev,
  ROUND(AVG("List Price Revenue" - "Total Logistics Revenue"), 2) AS avg_revenue_leakage,
  ROUND(100.0 * AVG("List Price Revenue" - "Total Logistics Revenue") / NULLIF(AVG("List Price Revenue"), 0), 2) AS pct_revenue_leakage
FROM lm
GROUP BY is_low