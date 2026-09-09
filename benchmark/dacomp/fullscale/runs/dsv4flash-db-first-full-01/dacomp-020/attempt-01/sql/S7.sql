SELECT "Mental health score" as mh, COUNT(*) as n, ROUND(AVG("Exam score"),3) as avg_exam,
       ROUND(AVG("Exam score"*"Exam score") - AVG("Exam score")*AVG("Exam score"),3) as var_exam
FROM sheet1
GROUP BY mh
ORDER BY mh