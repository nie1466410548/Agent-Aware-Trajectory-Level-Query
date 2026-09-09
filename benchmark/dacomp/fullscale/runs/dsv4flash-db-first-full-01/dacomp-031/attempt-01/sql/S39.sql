SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  Attrition,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(PercentSalaryHike),2) AS avg_hike,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(TrainingTimesLastYear),2) AS avg_training,
  ROUND(100.0*AVG(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END),1) AS pct_ot,
  ROUND(100.0*AVG(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END),1) AS pct_no_stock
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY Attrition