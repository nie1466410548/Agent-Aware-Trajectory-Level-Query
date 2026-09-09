
SELECT f."Season label" AS season, b."Agricultural Product Name" AS product,
       SUM(c."Sales Quantity (units)") AS total_qty
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", b."Agricultural Product Name"
