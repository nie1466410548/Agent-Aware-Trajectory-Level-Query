SELECT Attrition, COUNT(*) AS cnt,
  ROUND(AVG(MonthlyIncome),2) AS avg_income,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsAtCompany),2) AS avg_years_at_co,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(EnvironmentSatisfaction),2) AS avg_envsat,
  ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
  ROUND(AVG(OverTime='Yes')*100,2) AS pct_overtime,
  ROUND(AVG(StockOptionLevel=0)*100,2) AS pct_no_stock,
  ROUND(AVG(TrainingTimesLastYear),2) AS avg_training
FROM sheet1
GROUP BY Attrition