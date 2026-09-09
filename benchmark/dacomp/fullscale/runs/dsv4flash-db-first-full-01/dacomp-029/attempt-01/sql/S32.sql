SELECT 
  CASE 
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 1 THEN '0-1y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 1.5 THEN '1-1.5y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 2 THEN '1.5-2y'
    WHEN (julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25 < 3 THEN '2-3y'
    ELSE '3y+' END AS age_bucket,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100, 2) AS avg_retention_pct,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) / ((julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25), 2) AS retention_per_year,
  COUNT(*) AS cnt
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
  AND "Registration Date" IS NOT NULL AND "Posting Date" IS NOT NULL
GROUP BY age_bucket
ORDER BY age_bucket