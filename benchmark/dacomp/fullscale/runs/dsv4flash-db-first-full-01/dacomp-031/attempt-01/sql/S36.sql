
SELECT OverTime, StockOptionLevel, 
       COUNT(*) AS cnt,
       ROUND(100.0*SUM(CASE WHEN Attrition='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) AS attrition_rate
FROM sheet1
GROUP BY OverTime, StockOptionLevel
ORDER BY OverTime, StockOptionLevel
