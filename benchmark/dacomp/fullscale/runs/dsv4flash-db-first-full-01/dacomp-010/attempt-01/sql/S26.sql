SELECT c."Buyer Type", COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Buyer Type"
ORDER BY total_qty DESC