SELECT "Index", COUNT(*) AS n, MIN("Date") AS min_d, MAX("Date") AS max_d FROM index_trade GROUP BY "Index" ORDER BY "Index"
