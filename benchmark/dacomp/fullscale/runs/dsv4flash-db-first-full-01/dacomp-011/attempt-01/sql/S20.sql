SELECT 
  CASE 
    WHEN "Mental health score" <= 3 THEN 'Low (0-3)'
    WHEN "Mental health score" <= 6 THEN 'Medium (4-6)'
    ELSE 'High (7-10)'
  END AS mh_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study
FROM sheet1
GROUP BY mh_cat
ORDER BY avg_exam DESC