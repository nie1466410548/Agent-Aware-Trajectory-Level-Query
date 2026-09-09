
WITH proc_items AS (
  SELECT s."Item Code", SUM(s."Sales volume (kg)") as vol_0630
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
),
summer_sales AS (
  SELECT s."Item Code",
    s."Sales volume (kg)" as vol,
    s."Unit price (yuan/kg)" as up,
    pp."Wholesale price (yuan/kg)" as wp,
    pl."Loss Rate (%)" as lr,
    strftime('%Y', s."Sales Date") as yr,
    s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) as profit
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
),
y2022 AS (
  SELECT "Item Code", COUNT(*) n22, AVG(profit) avgp22,
    SUM(CASE WHEN profit<0 THEN 1 ELSE 0 END)*100.0/COUNT(*) pct22,
    SUM(vol*profit) tot22
  FROM summer_sales WHERE yr='2022' GROUP BY "Item Code"
)
SELECT pi."Item Code", p."Item Name", ROUND(pi.vol_0630,2) vol_0630,
  y.n22, ROUND(y.avgp22,3) avgp22, ROUND(y.pct22,1) pct22, ROUND(y.tot22,2) tot22
FROM proc_items pi
LEFT JOIN product_information p ON pi."Item Code" = p."Item Code"
LEFT JOIN y2022 y ON pi."Item Code" = y."Item Code"
ORDER BY COALESCE(y.avgp22, 999) ASC
