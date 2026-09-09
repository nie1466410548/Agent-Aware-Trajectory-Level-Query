SELECT 
  "Vehicle Class",
  COUNT(*) AS cnt,
  COUNT("Registration Date") AS cnt_reg,
  ROUND(AVG(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL))*100,2) AS avg_retention_pct
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
  AND "Registration Date" IS NOT NULL
GROUP BY "Vehicle Class"
ORDER BY avg_retention_pct DESC