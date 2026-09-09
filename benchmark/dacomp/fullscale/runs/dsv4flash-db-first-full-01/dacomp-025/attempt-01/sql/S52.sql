SELECT s."Item Code", p."Item Name",
  COUNT(*) as n_sales,
  SUM(s."Sales volume (kg)") as total_vol,
  ROUND(SUM(s."Sales volume (kg)" * (s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0)),2) as total_profit_loss,
  ROUND(AVG(s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0),3) as avg_profit_per_kg,
  SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) THEN 1 ELSE 0 END) as n_loss_sales
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
  AND s."Sales type" = 'Sale'
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
  AND pl."Loss Rate (%)" IS NOT NULL
GROUP BY s."Item Code"
HAVING total_profit_loss < 0 OR n_loss_sales > 0
ORDER BY total_profit_loss ASC