-- Check July 2022 for portion items correctly
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" LIKE '%(portion)%'
  AND s."Sales Date" BETWEEN '2022-06-01' AND '2022-09-01'
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym