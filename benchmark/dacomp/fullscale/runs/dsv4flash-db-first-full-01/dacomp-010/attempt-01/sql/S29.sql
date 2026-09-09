SELECT c."Sales Channel",
       ROUND(AVG(f."Market price (CNY/kg)"),2) AS avg_market_price,
       f."Inventory status",
       COUNT(*) AS n
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", f."Inventory status"
ORDER BY c."Sales Channel", n DESC