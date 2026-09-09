WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_sales AS (
  SELECT s."Item Code", s."Unit price (yuan/kg)" as up, pp."Wholesale price (yuan/kg)" as wp, pl."Loss Rate (%)" as lr
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code",
  COUNT(*) as n_sales,
  SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END) as n_loss,
  ROUND(100.0*SUM(CASE WHEN up < wp/(1.0-lr/100.0) THEN 1 ELSE 0 END)/COUNT(*),1) as pct_loss,
  ROUND(AVG(up - wp/(1.0-lr/100.0)),3) as avg_profit_per_kg,
  ROUND(MIN(up - wp/(1.0-lr/100.0)),3) as min_profit
FROM summer_sales
GROUP BY "Item Code"
ORDER BY pct_loss DESC, n_sales DESC