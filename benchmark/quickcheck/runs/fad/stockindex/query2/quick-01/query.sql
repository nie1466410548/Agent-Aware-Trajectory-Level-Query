SELECT "Index",
       SUM(CASE WHEN "Close" > "Open" THEN 1 ELSE 0 END) AS up_days,
       SUM(CASE WHEN "Close" < "Open" THEN 1 ELSE 0 END) AS down_days,
       SUM(CASE WHEN "Close" = "Open" THEN 1 ELSE 0 END) AS flat_days,
       COUNT(*) AS total_days
FROM index_trade
WHERE "Index" IN ('NYA','IXIC','GSPTSE')
  AND "Date" >= '2018-01-01' AND "Date" < '2019-01-01'
GROUP BY "Index"
ORDER BY "Index";
