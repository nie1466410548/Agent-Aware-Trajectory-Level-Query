SELECT 
  ROUND(SUM(("Exam score"-avg_e)*("Daily study time"-avg_s))/ (COUNT(*)*STDDEV_agg("Exam score")*STDDEV_agg("Daily study time")),4) AS corr_study
FROM sheet1