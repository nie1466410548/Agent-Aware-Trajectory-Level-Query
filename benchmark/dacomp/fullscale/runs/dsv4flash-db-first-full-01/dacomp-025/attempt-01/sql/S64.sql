WITH proc_items AS (
  SELECT DISTINCT s."Item Code"
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30'
),
summer_analysis AS (
  SELECT s."Item Code",
    strftime('%m', s."Sales Date") as mo,
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  JOIN proc_items pi ON s."Item Code" = pi."Item Code"
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Sales type" = 'Sale'
    AND s."Sales Date" >= '2022-07-01' AND s."Sales Date" < '2022-09-01'
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT "Item Code", mo, COUNT(*) as n,
  ROUND(AVG(profit),3) as avg_profit,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) as pct_loss
FROM summer_analysis
GROUP BY "Item Code", mo
HAVING n >= 20
ORDER BY avg_profit ASC
LIMIT 20