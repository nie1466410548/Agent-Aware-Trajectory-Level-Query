-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.
PRAGMA temp_store=MEMORY;
BEGIN;

-- S3
SELECT COUNT(*) AS total_rows FROM sheet1;

-- S4
SELECT "Parents' education level" AS parent_edu, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(MIN("Exam score"),2) AS min_exam, ROUND(MAX("Exam score"),2) AS max_exam FROM sheet1 GROUP BY "Parents' education level" ORDER BY avg_exam DESC;

-- S5
SELECT 'Gender' AS col, Gender AS val, COUNT(*) AS n FROM sheet1 GROUP BY Gender
UNION ALL
SELECT 'Part-time job', "Part-time job", COUNT(*) FROM sheet1 GROUP BY "Part-time job"
UNION ALL
SELECT 'Diet quality', "Diet quality", COUNT(*) FROM sheet1 GROUP BY "Diet quality"
UNION ALL
SELECT 'Internet quality', "Internet quality", COUNT(*) FROM sheet1 GROUP BY "Internet quality"
UNION ALL
SELECT 'Extracurricular', "Extracurricular activity participation", COUNT(*) FROM sheet1 GROUP BY "Extracurricular activity participation";

-- S6
SELECT ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(MIN("Exam score"),2) AS min_exam, ROUND(MAX("Exam score"),2) AS max_exam, ROUND(AVG("Daily study time"),2) AS avg_study, ROUND(AVG("Social media usage time"),2) AS avg_social, ROUND(AVG("Attendance rate"),2) AS avg_attendance, ROUND(AVG("Sleep duration"),2) AS avg_sleep, ROUND(AVG("Exercise frequency"),2) AS avg_exercise, ROUND(AVG("Mental health score"),2) AS avg_mh FROM sheet1;

-- S8
SELECT "Parents' education level" AS parent_edu, Gender, ROUND(AVG("Exam score"),2) AS avg_exam, COUNT(*) AS n FROM sheet1 GROUP BY "Parents' education level", Gender ORDER BY parent_edu, Gender;

-- S9
SELECT "Parents' education level" AS parent_edu, 
  ROUND(AVG("Daily study time"),2) AS avg_study,
  ROUND(AVG("Social media usage time"),2) AS avg_social,
  ROUND(AVG("Attendance rate"),2) AS avg_attendance,
  ROUND(AVG("Sleep duration"),2) AS avg_sleep,
  ROUND(AVG("Exercise frequency"),2) AS avg_exercise,
  ROUND(AVG("Mental health score"),2) AS avg_mh
FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu;

-- S11
SELECT COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam, ROUND(MIN("Exam score"),2) AS min_exam, ROUND(MAX("Exam score"),2) AS max_exam FROM sheet1 WHERE "Parents' education level" IS NOT NULL;

-- S12
WITH stats AS (
  SELECT 
    COUNT(*) AS n,
    AVG("Exam score") AS m_e,
    AVG("Daily study time") AS m_s,
    AVG("Social media usage time") AS m_so,
    AVG("Attendance rate") AS m_a,
    AVG("Sleep duration") AS m_sl,
    AVG("Exercise frequency") AS m_ex,
    AVG("Mental health score") AS m_mh,
    AVG(Age) AS m_age
  FROM sheet1
)
SELECT
  ROUND(SUM(("Exam score"-m_e)*("Daily study time"-m_s))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Daily study time"-m_s)*("Daily study time"-m_s))),4) AS corr_study,
  ROUND(SUM(("Exam score"-m_e)*("Social media usage time"-m_so))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Social media usage time"-m_so)*("Social media usage time"-m_so))),4) AS corr_social,
  ROUND(SUM(("Exam score"-m_e)*("Attendance rate"-m_a))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Attendance rate"-m_a)*("Attendance rate"-m_a))),4) AS corr_attendance,
  ROUND(SUM(("Exam score"-m_e)*("Sleep duration"-m_sl))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Sleep duration"-m_sl)*("Sleep duration"-m_sl))),4) AS corr_sleep,
  ROUND(SUM(("Exam score"-m_e)*("Exercise frequency"-m_ex))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Exercise frequency"-m_ex)*("Exercise frequency"-m_ex))),4) AS corr_exercise,
  ROUND(SUM(("Exam score"-m_e)*("Mental health score"-m_mh))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM(("Mental health score"-m_mh)*("Mental health score"-m_mh))),4) AS corr_mh,
  ROUND(SUM(("Exam score"-m_e)*(Age-m_age))/SQRT(SUM(("Exam score"-m_e)*("Exam score"-m_e))*SUM((Age-m_age)*(Age-m_age))),4) AS corr_age
FROM sheet1, stats;

-- S13
SELECT "Parents' education level" AS parent_edu, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND((SUM("Exam score"*"Exam score") - SUM("Exam score")*SUM("Exam score")/COUNT(*)) / (COUNT(*)-1), 2) AS var_exam
FROM sheet1 GROUP BY "Parents' education level" ORDER BY parent_edu;

-- S15
SELECT "Diet quality" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY "Diet quality" ORDER BY avg_exam DESC;

-- S16
SELECT "Internet quality" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY "Internet quality" ORDER BY avg_exam DESC;

-- S17
SELECT "Extracurricular activity participation" AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY "Extracurricular activity participation" ORDER BY avg_exam DESC;

-- S18
SELECT Gender AS val, COUNT(*) AS n, ROUND(AVG("Exam score"),2) AS avg_exam FROM sheet1 GROUP BY Gender ORDER BY avg_exam DESC;

-- S19
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
ORDER BY avg_exam DESC;

-- S20
SELECT 
  CASE 
    WHEN "Mental health score" <= 3 THEN 'Low (0-3)'
    WHEN "Mental health score" <= 6 THEN 'Medium (4-6)'
    ELSE 'High (7-10)'
  END AS mh_cat,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam,
  ROUND(AVG("Daily study time"),2) AS avg_study
FROM sheet1
GROUP BY mh_cat
ORDER BY avg_exam DESC;

-- S21
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
ORDER BY avg_exam DESC;

-- S22
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
ORDER BY parent_edu, study_cat;

-- S23
SELECT "Parents' education level" AS parent_edu,
  "Part-time job" AS pt_job,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, pt_job
ORDER BY parent_edu, pt_job;

-- S24
SELECT "Parents' education level" AS parent_edu,
  "Diet quality" AS diet,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, diet
ORDER BY parent_edu, diet;

-- S25
SELECT * FROM sheet1;

-- S26
SELECT * FROM sheet1;

-- S27
SELECT * FROM sheet1;

-- S28
SELECT * FROM sheet1;

-- S29
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
ORDER BY avg_exam DESC;

-- S30
SELECT 
  CASE WHEN "Parents' education level" IS NULL THEN 'Missing' ELSE "Parents' education level" END AS parent_edu,
  "Diet quality" AS diet,
  COUNT(*) AS n,
  ROUND(AVG("Exam score"),2) AS avg_exam
FROM sheet1
GROUP BY parent_edu, diet
ORDER BY parent_edu, diet;


COMMIT;
