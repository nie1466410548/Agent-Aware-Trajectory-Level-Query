SELECT 
  CASE 
    WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
    WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
    WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
    WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
    ELSE '20+ years'
  END AS tenure_band,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(JobLevel),2) AS avg_job_level,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role,
  ROUND(AVG(YearsWithCurrManager),2) AS avg_years_with_mgr,
  ROUND(AVG(StockOptionLevel),2) AS avg_stock,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)