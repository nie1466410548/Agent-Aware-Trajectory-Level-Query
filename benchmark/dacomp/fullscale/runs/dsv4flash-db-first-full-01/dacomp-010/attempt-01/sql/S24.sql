SELECT b."Agricultural Product Name", c."Sales Channel",
       ROUND(SUM(f."Customer Satisfaction"='Very satisfied')*1.0/COUNT(*),3) AS very_sat_rate,
       ROUND(SUM(f."Customer Satisfaction"='Satisfied')*1.0/COUNT(*),3) AS sat_rate,
       ROUND(SUM(f."Repurchase intention" IN ('Very high','Relatively high'))*1.0/COUNT(*),3) AS repurchase_high
FROM core_transaction_information c
JOIN basic_product_information b ON c."Transaction Number" = b."Transaction Number"
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
WHERE strftime('%Y', c."Transaction Date") = '2024'
GROUP BY b."Agricultural Product Name", c."Sales Channel"
ORDER BY b."Agricultural Product Name", repurchase_high DESC