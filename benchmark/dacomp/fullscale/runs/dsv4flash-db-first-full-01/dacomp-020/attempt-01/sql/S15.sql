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
FROM sheet1