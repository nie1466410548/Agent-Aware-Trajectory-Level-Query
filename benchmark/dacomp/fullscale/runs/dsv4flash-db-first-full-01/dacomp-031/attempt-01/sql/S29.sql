SELECT JobRole,
  COUNT(*) AS cnt,
  ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
  ROUND(AVG(YearsAtCompany),2) AS avg_tenure
FROM sheet1
GROUP BY JobRole
ORDER BY attrition_rate_pct DESC