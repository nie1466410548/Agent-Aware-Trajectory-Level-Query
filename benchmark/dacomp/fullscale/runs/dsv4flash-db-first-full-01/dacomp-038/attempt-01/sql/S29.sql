SELECT "Promotion Date", Strategy, COUNT(*) AS n, ROUND(SUM("Spend (Yuan)"),1) AS spend
FROM sheet1 WHERE Strategy LIKE 'Search%'
GROUP BY "Promotion Date", Strategy ORDER BY "Promotion Date", Strategy