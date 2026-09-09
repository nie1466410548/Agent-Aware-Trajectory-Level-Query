SELECT pi."Category Name", strftime('%m', "Sales Date") AS month,
       ROUND(SUM(s."Sales volume (kg)"),1) AS vol_kg
FROM sales_records s
JOIN product_information pi ON s."Item Code" = pi."Item Code"
GROUP BY pi."Category Name", month
ORDER BY pi."Category Name", month