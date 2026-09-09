SELECT "Parents' education level" AS parent_edu, 
  ROUND(AVG("Daily study time"),2) AS avg_study,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_attendance,
  ROUND(AVG("Sleep duration"),2) AS avg_sleep,
  ROUND(AVG("Exercise frequency"),2) AS avg_exercise,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu