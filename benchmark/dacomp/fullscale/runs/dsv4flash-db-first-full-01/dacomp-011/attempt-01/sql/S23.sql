SELECT "Parents' education level" AS parent_edu,
  "Part-time job" AS pt_job,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, pt_job
ORDER BY parent_edu, pt_job