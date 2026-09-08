SELECT
  COUNT(*) AS n,
  SUM(CASE WHEN "Profit" < 0 THEN 1 ELSE 0 END) AS neg_profit,
  SUM(CASE WHEN "Profit Margin" > 1 OR "Profit Margin" < 0 THEN 1 ELSE 0 END) AS bad_margin,
  ROUND(MIN("Profit"),2) AS min_profit,
  ROUND(MAX("Profit"),2) AS max_profit,
  ROUND(MIN("Profit Margin"),4) AS min_margin,
  ROUND(MAX("Profit Margin"),4) AS max_margin,
  ROUND(AVG("Profit"),2) AS avg_profit
FROM sheet1
WHERE "Destination" LIKE 'South China%'