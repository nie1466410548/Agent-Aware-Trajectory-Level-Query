WITH sc AS (SELECT * FROM sheet1 WHERE "Destination" LIKE 'South China%'),
ranked AS (
  SELECT "Profit", NTILE(100) OVER (ORDER BY "Profit") AS pct
  FROM sc
),
tot AS (SELECT SUM("Profit") AS t FROM sc)
SELECT pct, ROUND(SUM("Profit"),0) AS profit, ROUND(100.0*SUM("Profit")/(SELECT t FROM tot),2) AS pct_of_total, COUNT(*) AS n
FROM ranked
GROUP BY pct
HAVING pct IN (1,2,5,10,20,50,80,90,95,98,99,100)
ORDER BY pct