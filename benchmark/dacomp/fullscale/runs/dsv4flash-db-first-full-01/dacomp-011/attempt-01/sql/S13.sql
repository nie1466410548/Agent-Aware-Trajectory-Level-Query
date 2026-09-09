SELECT "Parents' education level" AS parent_edu, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND((SUM("Exam score"*"Exam score") - SUM("Exam score")*SUM("Exam score")/COUNT(*)) / (COUNT(*)-1), 2) AS var_exam
FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu