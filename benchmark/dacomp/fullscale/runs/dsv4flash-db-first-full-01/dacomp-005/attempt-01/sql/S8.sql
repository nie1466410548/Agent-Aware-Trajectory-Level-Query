WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  is_low,
  COUNT(*) AS n,
  ROUND(AVG("Sales Quantity"),2) AS avg_sales_qty,
  ROUND(AVG("Logistics Unit Price"),2) AS avg_unit_price,
  ROUND(AVG("List Price Revenue"),2) AS avg_list_price_rev,
  ROUND(AVG("Logistics Value-Added Service Revenue"),2) AS avg_vas_rev,
  ROUND(AVG("Discount Amount"),2) AS avg_discount,
  ROUND(AVG("Discount Amount") / AVG("List Price Revenue") * 100,2) AS discount_pct_of_list,
  ROUND(AVG("Total Logistics Revenue"),2) AS avg_total_rev,
  ROUND(AVG("Freight Cost"),2) AS avg_freight,
  ROUND(AVG("Warehousing Cost"),2) AS avg_warehousing,
  ROUND(AVG("Other Operating Costs"),2) AS avg_other_op,
  ROUND(AVG("Total Logistics Cost"),2) AS avg_total_cost,
  ROUND(AVG("Profit"),2) AS avg_profit,
  ROUND(AVG("Profit Margin"),4) AS avg_profit_margin
FROM lm
GROUP BY is_low