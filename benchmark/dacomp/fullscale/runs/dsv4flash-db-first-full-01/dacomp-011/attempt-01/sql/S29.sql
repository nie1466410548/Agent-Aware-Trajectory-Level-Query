SELECT 
  CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS parent_edu,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_att,
  ROUND(AVG("Sleep duration"),2) AS avg_sleep,
  ROUND(AVG("Exercise frequency"),2) AS avg_ex,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1
GROUP BY parent_edu
ORDER BY avg_exam DESC