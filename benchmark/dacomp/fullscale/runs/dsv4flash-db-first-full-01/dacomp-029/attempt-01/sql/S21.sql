SELECT 
  "Vehicle Class",
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100,2) AS avg_retention_pct,
  ROUND(AVG(julianday("Posting Date") - julianday("Registration Date"))/365.25, 2) AS avg_age,
  ROUND(AVG(Price),2) AS avg_price_wan,
  COUNT(*) AS cnt
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY "Vehicle Class"
ORDER BY avg_retention_pct DESC