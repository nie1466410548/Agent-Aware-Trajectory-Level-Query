SELECT 
  CASE 
    WHEN "WLTC Electric Range (km)" = '/' OR "WLTC Electric Range (km)" IS NULL OR "WLTC Electric Range (km)" = '' THEN 'unknown'
    WHEN CAST("WLTC Electric Range (km)" AS REAL) >= 300 THEN '300+ km'
    WHEN CAST("WLTC Electric Range (km)" AS REAL) >= 200 THEN '200-300 km'
    WHEN CAST("WLTC Electric Range (km)" AS REAL) >= 100 THEN '100-200 km'
    ELSE '0-100 km' END AS range_bucket,
  COUNT(*) AS cnt,
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY range_bucket
ORDER BY avg_retention_pct DESC