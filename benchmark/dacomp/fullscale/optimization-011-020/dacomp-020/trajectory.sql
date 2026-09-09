-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.
PRAGMA temp_store=MEMORY;
BEGIN;

-- S3
SELECT * FROM sheet1 LIMIT 10;

-- S4
SELECT COUNT(*) as total_rows FROM sheet1;

-- S5
SELECT MIN("Mental health score") as min_mh, MAX("Mental health score") as max_mh, AVG("Mental health score") as avg_mh, 
       MIN("Exam score") as min_exam, MAX("Exam score") as max_exam, AVG("Exam score") as avg_exam
FROM sheet1;

-- S7
SELECT "Mental health score" as mh, COUNT(*) as n, ROUND(AVG("Exam score"),3) as avg_exam,
       ROUND(AVG("Exam score"*"Exam score") - AVG("Exam score")*AVG("Exam score"),3) as var_exam
FROM sheet1
GROUP BY mh
ORDER BY mh;

-- S8
SELECT 
  SUM(("Mental health score" - mh_mean) * ("Exam score" - exam_mean)) / (COUNT(*) - 1) as cov,
  SQRT(SUM(("Mental health score" - mh_mean)*("Mental health score" - mh_mean))/(COUNT(*)-1)) as sd_mh,
  SQRT(SUM(("Exam score" - exam_mean)*("Exam score" - exam_mean))/(COUNT(*)-1)) as sd_exam
FROM sheet1, (SELECT AVG("Mental health score") as mh_mean, AVG("Exam score") as exam_mean FROM sheet1);

-- S9
SELECT "Gender", COUNT(*) as n FROM sheet1 GROUP BY "Gender";

-- S10
SELECT "Part-time job", COUNT(*) as n FROM sheet1 GROUP BY "Part-time job";

-- S11
SELECT "Diet quality", COUNT(*) as n FROM sheet1 GROUP BY "Diet quality";

-- S12
SELECT "Parents' education level", COUNT(*) as n FROM sheet1 GROUP BY "Parents' education level";

-- S13
SELECT "Internet quality", COUNT(*) as n FROM sheet1 GROUP BY "Internet quality";

-- S14
SELECT "Extracurricular activity participation", COUNT(*) as n FROM sheet1 GROUP BY "Extracurricular activity participation";

-- S15
SELECT 
  SUM(CASE WHEN "Age" IS NULL THEN 1 ELSE 0 END) as age_null,
  SUM(CASE WHEN "Daily study time" IS NULL THEN 1 ELSE 0 END) as study_null,
  SUM(CASE WHEN "Social media usage time" IS NULL THEN 1 ELSE 0 END) as sm_null,
  SUM(CASE WHEN "Attendance rate" IS NULL THEN 1 ELSE 0 END) as att_null,
  SUM(CASE WHEN "Sleep duration" IS NULL THEN 1 ELSE 0 END) as sleep_null,
  SUM(CASE WHEN "Exercise frequency" IS NULL THEN 1 ELSE 0 END) as ex_null,
  SUM(CASE WHEN "Mental health score" IS NULL THEN 1 ELSE 0 END) as mh_null,
  SUM(CASE WHEN "Exam score" IS NULL THEN 1 ELSE 0 END) as exam_null,
  SUM(CASE WHEN "Part-time job" IS NULL THEN 1 ELSE 0 END) as pt_null,
  SUM(CASE WHEN "Gender" IS NULL THEN 1 ELSE 0 END) as gender_null,
  SUM(CASE WHEN "Internet quality" IS NULL THEN 1 ELSE 0 END) as iq_null,
  SUM(CASE WHEN "Diet quality" IS NULL THEN 1 ELSE 0 END) as diet_null
FROM sheet1;

-- S16
SELECT 
  MIN("Daily study time") as mn_study, MAX("Daily study time") as mx_study, AVG("Daily study time") as avg_study,
  MIN("Social media usage time") as mn_sm, MAX("Social media usage time") as mx_sm, AVG("Social media usage time") as avg_sm,
  MIN("Attendance rate") as mn_att, MAX("Attendance rate") as mx_att, AVG("Attendance rate") as avg_att,
  MIN("Sleep duration") as mn_sleep, MAX("Sleep duration") as mx_sleep, AVG("Sleep duration") as avg_sleep,
  MIN("Exercise frequency") as mn_ex, MAX("Exercise frequency") as mx_ex, AVG("Exercise frequency") as avg_ex,
  MIN("Age") as mn_age, MAX("Age") as mx_age, AVG("Age") as avg_age
FROM sheet1;

-- S17
SELECT * FROM sheet1;

-- S18
SELECT * FROM sheet1;


COMMIT;
