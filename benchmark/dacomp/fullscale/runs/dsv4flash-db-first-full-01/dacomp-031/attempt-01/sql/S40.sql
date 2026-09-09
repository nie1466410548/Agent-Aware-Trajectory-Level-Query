SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  Attrition,
  ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
  ROUND(AVG(YearsInCurrentRole),2) AS avg_years_in_role,
  ROUND(AVG(NumCompaniesWorked),2) AS avg_num_companies
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY Attrition