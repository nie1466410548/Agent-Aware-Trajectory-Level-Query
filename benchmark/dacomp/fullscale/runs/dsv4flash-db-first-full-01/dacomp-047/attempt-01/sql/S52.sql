-- Monthly pattern for Enoki Mushroom (box) and other top 2023 items
SELECT pi."Item Name", strftime('%m', s."Sales Date") AS mo, 
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN ('Enoki Mushroom (box)','White Button Mushroom (box)','Bird''s-eye Chili (portion)',
  'Spinach (portion)','Baby Bok Choy','Yunnan Leaf Lettuce (portion)','Yunnan Romaine Lettuce (portion)',
  'Milk Bok Choy (portion)','Wrinkled Pepper (portion)')
  AND s."Sales Date" >= '2022-01-01'
GROUP BY pi."Item Name", mo
ORDER BY pi."Item Name", mo