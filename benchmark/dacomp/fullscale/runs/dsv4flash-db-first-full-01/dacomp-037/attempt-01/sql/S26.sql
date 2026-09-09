SELECT "Medical history", "Drinking Status", COUNT(*) AS n
FROM health_status
GROUP BY "Medical history", "Drinking Status"
ORDER BY "Medical history", "Drinking Status"