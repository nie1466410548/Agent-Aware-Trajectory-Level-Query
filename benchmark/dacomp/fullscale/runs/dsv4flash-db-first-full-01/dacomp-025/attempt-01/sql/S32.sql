SELECT DISTINCT s."Item Code", p."Item Name", SUM(s."Sales volume (kg)") as total_vol
FROM sales_records s
LEFT JOIN product_information p ON s."Item Code" = p."Item Code"
WHERE date(s."Sales Date") = '2023-06-30'
GROUP BY s."Item Code"
ORDER BY total_vol DESC