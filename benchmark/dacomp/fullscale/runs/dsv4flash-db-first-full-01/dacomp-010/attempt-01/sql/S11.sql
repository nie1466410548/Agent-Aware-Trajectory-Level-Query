SELECT strftime('%Y', c."Transaction Date") AS yr, f."Season label", COUNT(*) AS n
FROM core_transaction_information c
JOIN market_and_quality_feedback_inf f ON c."Transaction Number" = f."Transaction Number"
GROUP BY yr, f."Season label"
ORDER BY yr, f."Season label"