SELECT YearsSinceLastPromotion, 
       COUNT(*) AS cnt,
       SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END) AS leavers,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS attrition_rate_pct,
       ROUND(AVG(MonthlyIncome),0) AS avg_income
FROM sheet1
GROUP BY YearsSinceLastPromotion
HAVING cnt >= 20
ORDER BY YearsSinceLastPromotion