WITH t AS (
  SELECT "Index", "Date", "Open", "Close",
         LAG("Close") OVER (PARTITION BY "Index" ORDER BY "Date") AS prev_close
  FROM index_trade
  WHERE "Index" IN ('NYA','IXIC','GSPTSE')
    AND "Date" >= '2017-11-01' AND "Date" < '2019-01-01'
)
SELECT "Index",
       MIN("Date") AS first_date, MAX("Date") AS last_date, COUNT(*) AS n,
       SUM(CASE WHEN "Close" > prev_close THEN 1 ELSE 0 END) AS up_vs_prev,
       SUM(CASE WHEN "Close" < prev_close THEN 1 ELSE 0 END) AS down_vs_prev
FROM t
WHERE "Date" >= '2018-01-01'
GROUP BY "Index"
ORDER BY "Index";
