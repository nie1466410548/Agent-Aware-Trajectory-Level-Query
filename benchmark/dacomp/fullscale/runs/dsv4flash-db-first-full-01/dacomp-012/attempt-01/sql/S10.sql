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
SELECT 
  interval,
  COUNT(*) AS n,
  ROUND(AVG(carat),3) AS avg_carat,
  ROUND(AVG(price),2) AS avg_price,
  ROUND(AVG(price/carat),2) AS avg_ppc,
  ROUND(MIN(price/carat),2) AS min_ppc,
  ROUND(MAX(price/carat),2) AS max_ppc,
  ROUND(sqrt(AVG((price/carat)*(price/carat)) - AVG(price/carat)*AVG(price/carat)),2) AS sd_ppc,
  ROUND(AVG(price/carat)/sqrt(AVG((price/carat)*(price/carat)) - AVG(price/carat)*AVG(price/carat)),2) AS cv
FROM buckets
GROUP BY interval
ORDER BY interval