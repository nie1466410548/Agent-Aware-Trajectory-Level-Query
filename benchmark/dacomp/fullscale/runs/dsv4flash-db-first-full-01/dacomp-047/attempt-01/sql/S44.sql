-- When is Sweet Potato Vine Tips sold? Check its months
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Sweet Potato Vine Tips','Water Spinach','Yunnan Leaf Lettuce','Yellow Chinese Cabbage (2)')
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym DESC
LIMIT 60