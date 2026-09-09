SELECT 
  CASE 
    WHEN "Attendance rate" < 70 THEN '<70%'
    WHEN "Attendance rate" < 85 THEN '70-85%'
    WHEN "Attendance rate" < 95 THEN '85-95%'
    ELSE '95%+'
  END AS attendance_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study
FROM sheet1
GROUP BY attendance_cat
ORDER BY avg_exam DESC