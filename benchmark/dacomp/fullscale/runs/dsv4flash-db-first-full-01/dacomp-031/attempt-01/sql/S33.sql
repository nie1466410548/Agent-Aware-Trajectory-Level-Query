
SELECT CASE 
         WHEN YearsAtCompany BETWEEN 0 AND 5 THEN '0-5 years'
         WHEN YearsAtCompany BETWEEN 6 AND 10 THEN '6-10 years'
         WHEN YearsAtCompany BETWEEN 11 AND 15 THEN '11-15 years'
         WHEN YearsAtCompany BETWEEN 16 AND 20 THEN '16-20 years'
         WHEN YearsAtCompany > 20 THEN '20+ years'
       END AS tenure_band,
       COUNT(*) AS total,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate
FROM sheet1
GROUP BY tenure_band
ORDER BY MIN(YearsAtCompany)
