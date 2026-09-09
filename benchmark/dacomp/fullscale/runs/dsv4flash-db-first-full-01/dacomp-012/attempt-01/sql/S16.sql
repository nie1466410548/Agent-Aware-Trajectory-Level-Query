WITH b AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    "Cut (quality)" AS cut,
    "Color" AS color,
    "Clarity" AS clarity,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN '<=0.5'
      WHEN "Carat (diamond weight)" <= 1.0 THEN '0.51-1.0'
      WHEN "Carat (diamond weight)" <= 1.5 THEN '1.01-1.5'
      ELSE '>1.5'
    END AS interval
  FROM sheet1
)
SELECT interval, cut, COUNT(*) AS n, ROUND(AVG(price/carat),2) AS avg_ppc
FROM b
GROUP BY interval, cut
ORDER BY interval, avg_ppc DESC