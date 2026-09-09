SELECT 
  ROUND(AVG(retention),2) AS avg_retention,
  ROUND(MIN(retention),2) AS min_retention,
  ROUND(MAX(retention),2) AS max_retention,
  COUNT(*) AS cnt
FROM (
  SELECT 
    Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS retention
  FROM autohome
  WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)