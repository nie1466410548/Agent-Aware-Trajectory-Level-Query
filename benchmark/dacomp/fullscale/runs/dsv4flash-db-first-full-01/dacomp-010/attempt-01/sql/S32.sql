
SELECT c."Sales Channel" AS channel,
       c."Sales Quantity (units)" AS qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
  AND b."Agricultural Product Name" = 'Wheat'
  AND c."Transaction Status" = 'Completed'
ORDER BY c."Sales Channel", qty
