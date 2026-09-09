SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years band' ELSE 'other' END AS band,
  ROUND(AVG(CASE WHEN Attrition='Yes' THEN MonthlyIncome END),2) AS leaver_income,
  ROUND(AVG(CASE WHEN Attrition='No' THEN MonthlyIncome END),2) AS stayer_income,
  ROUND(AVG(CASE WHEN Attrition='Yes' THEN YearsSinceLastPromotion END),2) AS leaver_years_since_promo,
  ROUND(AVG(CASE WHEN Attrition='No' THEN YearsSinceLastPromotion END),2) AS stayer_years_since_promo,
  ROUND(AVG(CASE WHEN Attrition='Yes' THEN JobSatisfaction END),2) AS leaver_jobsat,
  ROUND(AVG(CASE WHEN Attrition='No' THEN JobSatisfaction END),2) AS stayer_jobsat
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY band