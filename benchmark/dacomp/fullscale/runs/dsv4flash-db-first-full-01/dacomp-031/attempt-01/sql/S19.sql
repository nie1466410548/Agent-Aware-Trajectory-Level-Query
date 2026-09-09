SELECT YearsAtCompany, COUNT(*) AS cnt,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct
FROM sheet1
GROUP BY YearsAtCompany
ORDER BY YearsAtCompany