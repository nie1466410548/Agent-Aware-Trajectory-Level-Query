SELECT 
  "Vehicle Class",
  COUNT(*) AS cnt,
  COUNT("Registration Date") AS cnt_reg,
  COUNT("Posting Date") AS cnt_post,
  ROUND(AVG(julianday("Posting Date") - julianday("Registration Date"))/365.25, 2) AS avg_age
FROM autohome
WHERE "New Car Price (incl. tax)" IS NOT NULL AND Price IS NOT NULL
GROUP BY "Vehicle Class"
ORDER BY avg_age DESC