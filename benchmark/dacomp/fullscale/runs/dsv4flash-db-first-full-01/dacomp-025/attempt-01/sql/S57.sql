WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)" as profit_simple
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  ROUND(AVG(profit_simple),3) as avg_profit_simple,
  ROUND(SUM(CASE WHEN profit_simple<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss_simple,
  ROUND(SUM(CASE WHEN profit_simple<0 THEN 1 ELSE 0 END),0) as n_loss_simple
FROM summer_analysis
GROUP BY "Item Code"
ORDER BY avg_profit_simple ASC
LIMIT 15