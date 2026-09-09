SELECT 
  CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END AS band,
  OverTime, Attrition, COUNT(*) AS cnt,
  ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (PARTITION BY CASE WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 band' ELSE 'other' END),2) AS pct
FROM sheet1
WHERE YearsAtCompany BETWEEN 6 AND 10
GROUP BY band, OverTime, Attrition
ORDER BY OverTime, Attrition