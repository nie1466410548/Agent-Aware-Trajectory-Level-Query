SELECT strftime('%Y-%m', created_at) AS month, COUNT(*) AS n
FROM qualtrics__contact
GROUP BY month ORDER BY month