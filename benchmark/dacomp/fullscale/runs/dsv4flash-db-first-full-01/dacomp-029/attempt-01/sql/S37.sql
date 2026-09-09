SELECT 
  "Registration Restrictions",
  ROUND(AVG(Price*10000 / np)*100, 2) AS avg_retention_pct,
  COUNT(*) AS cnt
FROM (
  SELECT *, CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np
  FROM autohome WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
)
GROUP BY "Registration Restrictions"
ORDER BY avg_retention_pct DESC