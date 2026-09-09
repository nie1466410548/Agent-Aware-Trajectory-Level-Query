SELECT pi."Item Name", COUNT(DISTINCT strftime('%Y', s."Sales Date")) AS n_years,
       SUM(CASE WHEN s."Sales Date">='2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) AS vol_2023,
       SUM(CASE WHEN s."Sales Date">='2022-01-01' AND s."Sales Date"<'2023-01-01' THEN s."Sales volume (kg)" ELSE 0 END) AS vol_2022
FROM sales_records s
JOIN product_information pi ON s."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN (
    'Yunnan Leaf Lettuce','Water Spinach','Sweet Potato Vine Tips',
    'Broccoli','Purple Eggplant (2)','Spiral chili pepper',
    'Yunnan Romaine Lettuce','Shanghai Bok Choy','Green-stem Loose Cauliflower',
    'Yellow Chinese Cabbage (2)','Napa Cabbage','Bubble Pepper (Premium)'
)
GROUP BY pi."Item Name" ORDER BY vol_2022 DESC