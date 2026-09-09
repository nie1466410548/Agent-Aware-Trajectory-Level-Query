SELECT "Mental health score", COUNT(*) as n, AVG("Exam score") as avg_exam, STDDEV("Exam score") as std_exam
FROM sheet1
GROUP BY "Mental health score"
ORDER BY "Mental health score"