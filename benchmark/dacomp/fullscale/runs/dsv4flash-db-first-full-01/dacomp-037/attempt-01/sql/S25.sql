SELECT "Medical history", "Smoking status", COUNT(*) AS n
FROM health_status
GROUP BY "Medical history", "Smoking status"
ORDER BY "Medical history", "Smoking status"