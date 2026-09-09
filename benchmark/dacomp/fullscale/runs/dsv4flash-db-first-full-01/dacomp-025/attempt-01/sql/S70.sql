WITH last_price AS (
  SELECT "Item Code", "Wholesale price (yuan/kg)" as wp
  FROM purchase_price
  WHERE ("Item Code", "Date") IN (
    SELECT "Item Code", MAX("Date")
    FROM purchase_price
    GROUP BY "Item Code"
  )
),
day_sales AS (
  SELECT s."Item Code",
    SUM(s."Sales volume (kg)") as vol,
    AVG(s."Unit price (yuan/kg)") as avg_up
  FROM sales_records s
  WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  GROUP BY s."Item Code"
)
SELECT ds."Item Code", p."Item Name",
  ROUND(ds.vol,2) as proc_vol_kg,
  ROUND(lp.wp,2) as last_wholesale,
  ROUND(pl."Loss Rate (%)",2) as loss_rate,
  ROUND(lp.wp/(1.0-pl."Loss Rate (%)"/100.0),2) as eff_cost,
  ROUND(ds.avg_up,2) as avg_sell_price,
  ROUND(ds.vol * (ds.avg_up - lp.wp/(1.0-pl."Loss Rate (%)"/100.0)),2) as expected_pnl_0701
FROM day_sales ds
LEFT JOIN last_price lp ON ds."Item Code" = lp."Item Code"
LEFT JOIN product_information p ON ds."Item Code" = p."Item Code"
LEFT JOIN product_loss pl ON ds."Item Code" = pl."Item Code"
WHERE lp.wp IS NOT NULL
ORDER BY expected_pnl_0701 ASC
LIMIT 10