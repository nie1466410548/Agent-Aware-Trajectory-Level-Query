SELECT profit, Sales, "Discount", profit*1.0/Sales AS margin,
       Sales - profit AS cost,
       "Quantity", "Shipping Cost"
FROM order_information 
WHERE "Product Category" = 'Home & Furniture' 
LIMIT 20