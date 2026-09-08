SELECT "Index", COUNT(*) AS n2018 FROM index_trade WHERE "Date" LIKE '%2018%' GROUP BY "Index" ORDER BY "Index"
