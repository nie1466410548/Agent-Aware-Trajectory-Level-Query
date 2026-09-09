SELECT c."Sales Channel", c."Buyer Type", COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price,
       ROUND(AVG(c."Total Transaction Amount"),2) AS avg_amount
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel", c."Buyer Type"
ORDER BY c."Sales Channel", total_qty DESC