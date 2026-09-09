SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  Attrition, 
  COUNT(*) AS cnt,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_envsat,
  ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
  ROUND(AVG(DistanceFromHome),2) AS avg_distance,
  ROUND(AVG(NumCompaniesWorked),2) AS avg_num_companies
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY Attrition