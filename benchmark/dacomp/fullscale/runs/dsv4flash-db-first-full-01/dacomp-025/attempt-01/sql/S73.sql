WITH summer_analysis AS (
  SELECT s."Item Code",
    strftime('%Y', s."Sales Date") as yr,
    strftime('%m', s."Sales Date") as mo,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
  FROM sales_records s
  LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
  LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
  WHERE s."Item Code" = 102900051000944
    AND s."Sales type" = 'Sale'
    AND (
      (s."Sales Date" >= '2020-07-01' AND s."Sales Date" < '2020-09-01')
      OR (s."Sales Date" >= '2021-06-01' AND s."Sales Date" < '2021-09-01')
      OR (s."Sales Date" >= '2022-06-01' AND s."Sales Date" < '2022-09-01')
    )
    AND pp."Wholesale price (yuan/kg)" IS NOT NULL
    AND pl."Loss Rate (%)" IS NOT NULL
)
SELECT yr, mo, COUNT(*) n, ROUND(AVG(profit),3) avg_profit,
  ROUND(SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss
FROM summer_analysis GROUP BY yr, mo ORDER BY yr, mo