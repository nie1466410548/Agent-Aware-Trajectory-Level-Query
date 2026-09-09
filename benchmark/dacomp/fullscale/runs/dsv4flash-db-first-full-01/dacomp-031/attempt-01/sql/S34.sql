
SELECT CASE WHEN YearsAtCompany >= 10 THEN '10+ Years' ELSE '<10 Years' END AS group_name,
       ROUND(AVG(MonthlyIncome),0) AS avg_income,
       ROUND(AVG(YearsSinceLastPromotion),2) AS avg_years_since_promo,
       ROUND(AVG(JobLevel),2) AS avg_job_level,
       ROUND(AVG(StockOptionLevel),2) AS avg_stock,
       ROUND(AVG(JobSatisfaction),2) AS avg_jobsat,
       ROUND(AVG(WorkLifeBalance),2) AS avg_wlb,
       ROUND(100.0*SUM(CASE WHEN OverTime='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_overtime,
       ROUND(100.0*SUM(CASE WHEN StockOptionLevel=0 THEN 1 ELSE 0 END)/COUNT(*),2) AS pct_no_stock,
       COUNT(*) AS cnt
FROM sheet1
GROUP BY group_name
ORDER BY group_name DESC
