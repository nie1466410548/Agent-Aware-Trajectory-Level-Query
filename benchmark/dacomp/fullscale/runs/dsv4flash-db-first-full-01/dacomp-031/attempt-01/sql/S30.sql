SELECT EducationField,
  COUNT(*) AS cnt,
  ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
  ROUND(AVG(YearsAtCompany),2) AS avg_tenure
FROM sheet1
GROUP BY EducationField
ORDER BY attrition_rate_pct DESC