-- 2023 trend for recommended items
SELECT pi."Item Name", strftime('%Y-%m', s."Sales Date") AS ym,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS avg_daily,
       ROUND(SUM(s."Sales volume (kg)"),1) AS month_vol
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE s."Sales Date" >= '2023-01-01'
  AND pi."Item Name" IN (
    'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
    'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
    'Yunnan Romaine Lettuce','Shanghai Bok Choy','Green-stem Loose Cauliflower'
  )
GROUP BY pi."Item Name", ym
ORDER BY pi."Item Name", ym