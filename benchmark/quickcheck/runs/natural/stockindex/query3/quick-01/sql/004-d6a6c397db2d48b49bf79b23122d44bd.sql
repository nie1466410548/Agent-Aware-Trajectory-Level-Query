SELECT "Index", MIN("Date") AS min_d, MAX("Date") AS max_d, COUNT(*) AS n FROM index_trade GROUP BY "Index" ORDER BY "Index"
