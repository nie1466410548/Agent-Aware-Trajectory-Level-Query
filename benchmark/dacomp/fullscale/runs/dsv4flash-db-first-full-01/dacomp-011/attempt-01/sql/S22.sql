SELECT "Parents' education level" AS parent_edu,
  CASE 
    WHEN "Daily study time" < 2 THEN '<2h'
    WHEN "Daily study time" < 4 THEN '2-4h'
    WHEN "Daily study time" < 6 THEN '4-6h'
    ELSE '6h+'
  END AS study_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, study_cat
ORDER BY parent_edu, study_cat