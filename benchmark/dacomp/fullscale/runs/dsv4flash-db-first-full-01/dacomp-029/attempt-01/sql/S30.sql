SELECT 
  Title,
  COUNT(*) AS cnt,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100, 2) AS avg_retention_pct,
  ROUND(AVG((julianday(TRIM("Posting Date")) - julianday("Registration Date"))/365.25), 2) AS avg_age,
  ROUND(AVG(Price), 2) AS avg_price_wan,
  ROUND(AVG(CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km','') AS REAL)*10000 
       WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',',''), ' km','') AS REAL) END), 0) AS avg_mileage_km
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY Title
HAVING COUNT(*) >= 3
ORDER BY avg_retention_pct DESC
LIMIT 25