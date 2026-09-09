SELECT 
  Attrition,
  ROUND(100.0*SUM(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_overtime,
  ROUND(100.0*SUM(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_no_stock,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo
FROM sheet1
WHERE YearsAtCompany >= 10
GROUP BY Attrition