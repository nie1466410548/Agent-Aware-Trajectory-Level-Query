SELECT pi."Item Code", pi."Item Name", pi."Category Name", pl."Loss Rate (%)"
FROM product_information pi
LEFT JOIN product_loss pl ON pi."Item Code" = pl."Item Code"
WHERE pi."Item Code" IN (102900011032732, 102900011034439, 102900005118824, 102900011034330, 102900011001691)