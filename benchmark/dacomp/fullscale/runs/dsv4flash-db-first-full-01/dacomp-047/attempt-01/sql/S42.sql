-- Historical July avg daily by year for recommended items
SELECT pi."Item Name", strftime('%Y', s."Sales Date") AS yr,
       ROUND(SUM(s."Sales volume (kg)")/COUNT(DISTINCT s."Sales Date"),2) AS july_avg_daily
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE strftime('%m', s."Sales Date")='07'
  AND pi."Item Name" IN (
    'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
    'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
    'Yunnan Romaine Lettuce','Shanghai Bok Choy','Green-stem Loose Cauliflower'
  )
GROUP BY pi."Item Name", yr
ORDER BY pi."Item Name", yr