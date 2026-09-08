SELECT "Index", MIN("Date") AS min_date, MAX("Date") AS max_date, COUNT(*) AS n FROM index_trade GROUP BY "Index" ORDER BY "Index";

