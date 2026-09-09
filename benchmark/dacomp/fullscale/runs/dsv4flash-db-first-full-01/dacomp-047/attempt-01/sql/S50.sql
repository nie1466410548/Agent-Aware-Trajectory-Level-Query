-- Check the July 2022 volumes for the currently-relevant items (both full and portion versions)
SELECT pi."Item Name", 
       ROUND(SUM(CASE WHEN strftime('%m',s."Sales Date")='07' AND strftime('%Y',s."Sales Date")='2022' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july22,
       ROUND(SUM(CASE WHEN strftime('%m',s."Sales Date")='07' AND strftime('%Y',s."Sales Date")='2021' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july21,
       ROUND(SUM(CASE WHEN strftime('%m',s."Sales Date")='07' AND strftime('%Y',s."Sales Date")='2020' THEN s."Sales volume (kg)" ELSE 0 END),1) AS july20
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN (
  'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
  'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
  'Yunnan Romaine Lettuce','Shanghai Bok Choy','Yellow Chinese Cabbage (2)',
  'Enoki Mushroom (box)','White Button Mushroom (box)','Baby Bok Choy',
  'Spinach (portion)','Milk Bok Choy (portion)','Yunnan Leaf Lettuce (portion)',
  'Yunnan Romaine Lettuce (portion)','Water Spinach (portion)','Bird''s-eye Chili (portion)',
  'Spiral chili pepper (portion)','Wuhu green pepper (1)'
)
GROUP BY pi."Item Name"
ORDER BY july22 DESC