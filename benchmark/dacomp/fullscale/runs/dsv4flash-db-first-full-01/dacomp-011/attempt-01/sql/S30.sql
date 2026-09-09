SELECT 
  CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS parent_edu,
  "Diet quality" AS diet,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, diet
ORDER BY parent_edu, diet