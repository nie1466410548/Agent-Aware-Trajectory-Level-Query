-- Monthly pattern for key items - focused on seasonal shape
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, 
       ROUND(AVG(CASE WHEN strftime('%Y', s."Sales Date")>='2022' THEN s."Sales volume (kg)"/COUNT(DISTINCT s."Sales Date") END),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
  'Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)','Milk Bok Choy (portion)',
  'Wrinkled Pepper (portion)','Water Spinach','Sweet Potato Vine Tips')
GROUP BY pi."Item Name", mo
ORDER BY pi."Item Name", CAST(mo AS INT)