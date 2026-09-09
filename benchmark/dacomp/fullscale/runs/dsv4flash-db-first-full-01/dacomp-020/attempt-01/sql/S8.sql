SELECT 
  SUM(("Mental health score" - mh_mean) * ("Exam score" - exam_mean)) / (COUNT(*) - 1) as cov,
  SQRT(SUM(("Mental health score" - mh_mean)*("Mental health score" - mh_mean))/(COUNT(*)-1)) as sd_mh,
  SQRT(SUM(("Exam score" - exam_mean)*("Exam score" - exam_mean))/(COUNT(*)-1)) as sd_exam
FROM sheet1, (SELECT AVG("Mental health score") as mh_mean, AVG("Exam score") as exam_mean FROM sheet1)