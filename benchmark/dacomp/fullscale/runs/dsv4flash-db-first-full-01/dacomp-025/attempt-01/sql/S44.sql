SELECT s."Item Code", p."Item Name",
  ROUND(SUM(s."Sales volume (kg)"),2) as vol_0630
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
GROUP BY s."Item Code"
ORDER BY vol_0630 DESC