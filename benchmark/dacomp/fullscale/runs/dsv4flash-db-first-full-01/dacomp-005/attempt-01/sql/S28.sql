WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  CASE 
    WHEN "Discount Amount" = 0 THEN '0%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.05 THEN '0-5%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.10 THEN '5-10%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.20 THEN '10-20%'
    WHEN "Discount Amount" / NULLIF("List Price Revenue", 0) < 0.30 THEN '20-30%'
    ELSE '30%+'
  END AS discount_band,
  COUNT(*) AS total,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_cnt,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0), 2) AS low_pct_in_band,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / 1243, 2) AS pct_of_all_low
FROM lm
GROUP BY discount_band
ORDER BY discount_band