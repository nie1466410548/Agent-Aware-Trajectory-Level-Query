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
FROM sheet1, stats