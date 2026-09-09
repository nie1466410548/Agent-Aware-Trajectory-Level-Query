SELECT c."Sales Channel",
       ROUND(AVG(f."Customer Satisfaction" <> 'Satisfied'),3) AS sat_rate,
       ROUND(AVG(f."Repurchase intention" IN ('Relatively high','High')),3) AS repurchase_rate
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024' AND b."Agricultural Product Name" = 'Wheat'
GROUP BY c."Sales Channel"
ORDER BY repurchase_rate DESC