SELECT "Destination" AS dest, COUNT(*) AS n, ROUND(SUM("Profit"),2) AS total_profit
FROM sheet1
GROUP BY "Destination"
ORDER BY n DESC