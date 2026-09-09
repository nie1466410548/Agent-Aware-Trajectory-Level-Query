WITH lm AS (
  SELECT *, CASE WHEN "Profit Margin" < 0.5 * (SELECT AVG("Profit Margin") FROM sheet1) THEN 1 ELSE 0 END AS is_low
  FROM sheet1
)
SELECT 
  SUBSTR("Destination", 1, INSTR("Destination", '-') - 1) AS region,
  SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) AS low_cnt,
  SUM(CASE WHEN is_low = 0 THEN 1 ELSE 0 END) AS normal_cnt,
  ROUND(100.0 * SUM(CASE WHEN is_low = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS low_pct,
  ROUND(AVG(CASE WHEN is_low = 1 THEN "Freight Cost" END), 2) AS lm_avg_freight,
  ROUND(AVG(CASE WHEN is_low = 0 THEN "Freight Cost" END), 2) AS normal_avg_freight
FROM lm
GROUP BY region
ORDER BY low_pct DESC