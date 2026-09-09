SELECT JobRole,
  COUNT(*) AS cnt,
  ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS attrition_rate,
  ROUND(AVG(MonthlyIncome),0) AS avg_income,
  ROUND(AVG(YearsAtCompany),1) AS avg_tenure
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY JobRole
ORDER BY attrition_rate DESC