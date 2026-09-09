SELECT MIN(YearsAtCompany) AS min_years, 
       MAX(YearsAtCompany) AS max_years, 
       ROUND(AVG(YearsAtCompany),2) AS avg_years,
       ROUND(AVG(CASE WHEN Attrition='No' THEN YearsAtCompany END),2) AS avg_years_stayers,
       ROUND(AVG(CASE WHEN Attrition='Yes' THEN YearsAtCompany END),2) AS avg_years_leavers
FROM sheet1