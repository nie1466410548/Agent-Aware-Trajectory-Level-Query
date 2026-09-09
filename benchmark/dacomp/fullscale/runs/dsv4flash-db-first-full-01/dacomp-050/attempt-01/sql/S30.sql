WITH stu AS (
  SELECT *, "Have you ever had suicidal thoughts?" AS suicidal FROM sheet1 
  WHERE "Working professional or student" = 'Student'
    AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
    AND "Sleep duration" IS NOT NULL
),
risk AS (
  SELECT *,
    (CASE WHEN "Academic stress" >= 4 THEN 1 ELSE 0 END +
     CASE WHEN "Financial stress" >= 4 THEN 1 ELSE 0 END +
     CASE WHEN "Dietary habits" = 'Unhealthy' THEN 1 ELSE 0 END +
     CASE WHEN "Sleep duration" = 'Less than 5 hours' THEN 1 ELSE 0 END) AS n_risk
  FROM stu
)
SELECT 
  CASE WHEN n_risk >= 3 THEN '3-4 risk factors' 
       WHEN n_risk = 2 THEN '2 risk factors'
       WHEN n_risk = 1 THEN '1 risk factor'
       ELSE '0 risk factors' END AS risk_band,
  COUNT(*) AS total,
  SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END) AS yes_n,
  ROUND(100.0*SUM(CASE WHEN suicidal='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS yes_pct
FROM risk
GROUP BY risk_band
ORDER BY yes_pct DESC