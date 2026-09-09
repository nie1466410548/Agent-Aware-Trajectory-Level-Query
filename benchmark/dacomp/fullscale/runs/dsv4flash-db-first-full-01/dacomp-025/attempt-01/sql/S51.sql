SELECT s."Item Code", p."Item Name",
  s."Unit price (yuan/kg)" as unit_price,
  pp."Wholesale price (yuan/kg)" as wholesale,
  pl."Loss Rate (%)" as loss_rate,
  ROUND(pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0),3) as eff_cost,
  ROUND(s."Unit price (yuan/kg)" - pp."Wholesale price (yuan/kg)"/(1.0-pl."Loss Rate (%)"/100.0),3) as profit_per_kg,
  s."Sales volume (kg)" as vol,
  s."Whether sold at a discount" as discount
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
LEFT JOIN purchase_price pp ON s."Item Code" = pp."Item Code" AND date(s."Sales Date") = date(pp."Date")
LEFT JOIN product_loss pl ON s."Item Code" = pl."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
  AND s."Sales type" = 'Sale'
  AND pp."Wholesale price (yuan/kg)" IS NOT NULL
  AND pl."Loss Rate (%)" IS NOT NULL
ORDER BY profit_per_kg ASC