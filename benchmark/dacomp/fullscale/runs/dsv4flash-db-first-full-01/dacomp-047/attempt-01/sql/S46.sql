-- Portion items: check their data span and July performance
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr, ROUND(SUM(s."Sales volume (kg)"),1) AS vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)',
  'Water Spinach (portion)','Shanghai Bok Choy (portion)','Sweet Potato Vine Tips (portion)',
  'Milk Bok Choy (portion)','Baby Green Bok Choy (portion)')
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr