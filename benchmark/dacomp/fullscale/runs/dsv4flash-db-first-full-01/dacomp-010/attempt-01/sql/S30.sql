SELECT c."Sales Channel", c."Payment Method",
       COUNT(*) AS n,
       ROUND(AVG(c."Payment Terms (days)"),1) AS avg_terms
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", c."Payment Method"
ORDER BY c."Sales Channel", n DESC