SELECT 
  CASE WHEN YearsAtCompany >= 10 THEN '10+ years' ELSE '<10 years' END AS tenure_group,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobLevel),2) AS avg_job_level,
  ROUND(AVG(StockOptionLevel),2) AS avg_stock_level,
  ROUND(AVG(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)*100,2) AS pct_no_stock,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(TotalWorkingYears),2) AS avg_total_work_years,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role
FROM sheet1
GROUP BY tenure_group