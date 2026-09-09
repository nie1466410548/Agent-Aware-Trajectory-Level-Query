SELECT "Product", "Quantity", Sales, profit, "Discount", profit*1.0/Sales AS margin
FROM order_information
WHERE "Product Category"='Home & Furniture' AND "Product"='Sofa Covers'
ORDER BY "Quantity", "Discount"