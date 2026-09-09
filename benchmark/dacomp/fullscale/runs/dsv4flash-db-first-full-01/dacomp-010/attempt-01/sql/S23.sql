SELECT b."Agricultural Product Name", c."Sales Channel",
       COUNT(*) AS n_trans,
       SUM(c."Sales Quantity (units)") AS total_qty,
       ROUND(AVG(c."Unit Price (yuan)"),2) AS avg_price,
       ROUND(SUM(c."Total Transaction Amount")/NULLIF(SUM(c."Sales Quantity (units)"),0),3) AS revenue_per_unit
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY b."Agricultural Product Name", c."Sales Channel"
ORDER BY b."Agricultural Product Name", total_qty DESC