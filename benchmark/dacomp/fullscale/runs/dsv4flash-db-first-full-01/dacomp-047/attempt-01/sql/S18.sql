SELECT s."Item Code", pi."Item Name", pi."Category Name",
       strftime('%Y', s."Sales Date") AS yr,
       strftime('%m', s."Sales Date") AS mo,
       ROUND(SUM(s."Sales volume (kg)"),2) AS vol_kg,
       ROUND(SUM(s."Sales volume (kg)"*s."Unit price (yuan/kg)"),2) AS revenue
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
GROUP BY s."Item Code", pi."Item Name", pi."Category Name", yr, mo
ORDER BY s."Item Code", yr, mo