SELECT
  CASE WHEN YearsAtCompany >= 10 AND Attrition='No' THEN '10+ Stayer'
       WHEN YearsAtCompany >= 10 AND Attrition='Yes' THEN '10+ Leaver'
       WHEN YearsAtCompany < 10 AND Attrition='No' THEN '<10 Stayer'
       ELSE '<10 Leaver' END AS segment,
  COUNT(*) AS cnt,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_envsat,
  ROUND(100.0*AVG(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END),1) AS pct_overtime
FROM sheet1
GROUP BY segment
ORDER BY segment