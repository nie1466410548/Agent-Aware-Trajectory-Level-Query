WITH buckets AS (
  SELECT 
    "Price (USD)" AS price,
    "Carat (diamond weight)" AS carat,
    CASE 
      WHEN "Carat (diamond weight)" <= 0.5 THEN 'A: <=0.5 ct'
      WHEN "Carat (diamond weight)" <= 1.0 THEN 'B: 0.51-1.0 ct'
      WHEN "Carat (diamond weight)" <= 1.5 THEN 'C: 1.01-1.5 ct'
      ELSE 'D: >1.5 ct'
    END AS interval
  FROM sheet1
)
SELECT interval, carat AS q, price_per_carat
FROM (
  SELECT interval, carat, price/carat AS price_per_carat,
    ROW_NUMBER() OVER (PARTITION BY interval ORDER BY price/carat) AS rn,
    COUNT(*) OVER (PARTITION BY interval) AS cnt
  FROM buckets
)
WHERE rn IN ((cnt+1)/2, (cnt+2)/2)
ORDER BY interval, q