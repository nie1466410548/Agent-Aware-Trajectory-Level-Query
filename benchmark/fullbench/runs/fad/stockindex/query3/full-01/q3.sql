SELECT "Index", MIN("Date") AS first_date, MAX("Date") AS last_date, COUNT(*) AS n
FROM index_trade
GROUP BY "Index"
ORDER BY "Index";
