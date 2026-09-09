SELECT c."Sales Channel", c."Promotion", COUNT(*) AS n,
       SUM(c."Sales Quantity (units)") AS total_qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", c."Promotion"
ORDER BY c."Sales Channel", c."Promotion"