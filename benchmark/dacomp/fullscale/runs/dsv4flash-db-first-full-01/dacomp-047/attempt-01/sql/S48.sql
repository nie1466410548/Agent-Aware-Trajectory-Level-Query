-- Actually, check if July data exists for these items
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, strftime('%Y', s."Sales Date") AS yr,
       ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)',
  'Water Spinach (portion)','Shanghai Bok Choy (portion)','Sweet Potato Vine Tips (portion)',
  'Milk Bok Choy (portion)','Baby Green Bok Choy (portion)')
  AND strftime('%m', s."Sales Date") = '07'
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr