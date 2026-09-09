SELECT 
  CASE 
    WHEN "Daily study time" < 2 THEN '<2h'
    WHEN "Daily study time" < 4 THEN '2-4h'
    WHEN "Daily study time" < 6 THEN '4-6h'
    ELSE '6h+'
  END AS study_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_attendance,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1
GROUP BY study_cat
ORDER BY avg_exam DESC