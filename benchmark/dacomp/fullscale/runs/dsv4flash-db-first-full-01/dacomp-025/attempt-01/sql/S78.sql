
SELECT s."Item Code", p."Item Name",
  COUNT(*) n_sales,
  ROUND(SUM(s."Sales volume (kg)"),2) vol,
  ROUND(AVG(s."Unit price (yuan/kg)"),2) avg_up,
  ROUND(AVG(pp."Wholesale price (yuan/kg)"),2) avg_wp,
  ROUND(AVG(pp."Wholesale price (yuan/kg)")/(1.0-pl."Loss Rate (%)"/100.0),2) avg_cost,
  ROUND(SUM(CASE WHEN s."Unit price (yuan/kg)" < pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0) THEN 1 ELSE 0 END)*100.0/COUNT(*),1) pct_loss_sales
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30' AND s."Sales type" = 'Sale'
  AND s."Item Code" IN (102900005118824, 102900011032732)
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
GROUP BY s."Item Code"
