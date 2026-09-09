-- Loss rates for top July items
SELECT pl."Item Code", pi."Item Name", pi."Category Name", pl."Loss Rate (%)"
FROM product_loss pl
JOIN product_information pi ON pl."Item Code"=pi."Item Code"
WHERE pi."Item Name" IN (
  'Yunnan Leaf Lettuce','Broccoli','Yunnan Romaine Lettuce','Wuhu green pepper (1)',
  'Peeled Lotus Root (1)','Sweet Potato Vine Tips','Water Spinach','Purple Eggplant (2)',
  'Yellow Chinese Cabbage (2)','Green-stem Loose Cauliflower','Bubble Pepper (Premium)',
  'Xixia shiitake (1)','Napa Cabbage','Spiral chili pepper','Shanghai Bok Choy',
  'Sweet Bok Choy','Lotus seed pod (piece)'
)
ORDER BY pl."Loss Rate (%)"