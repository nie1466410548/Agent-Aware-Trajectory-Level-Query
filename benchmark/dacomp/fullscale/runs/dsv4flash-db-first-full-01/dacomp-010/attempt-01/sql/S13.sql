SELECT f."Season label", b."Agricultural Product Name",
       COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_unit_price,
       SUM(c."Total Transaction Amount") AS total_amount
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY f."Season label", b."Agricultural Product Name"
ORDER BY f."Season label", total_qty DESC