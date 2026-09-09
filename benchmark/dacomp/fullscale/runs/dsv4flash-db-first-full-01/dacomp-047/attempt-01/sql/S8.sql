SELECT strftime('%Y-%m', "Sales Date") AS ym, pi."Category Name",
       ROUND(SUM(s."Sales volume (kg)"),1) AS vol_kg,
       COUNT(DISTINCT s."Item Code") AS n_items,
       ROUND(SUM(s."Sales volume (kg)" * s."Unit price (yuan/kg)"),0) AS revenue
FROM sales_records s
JOIN product_information pi ON s."Item Code" = pi."Item Code"
GROUP BY ym, pi."Category Name"
ORDER BY pi."Category Name", ym