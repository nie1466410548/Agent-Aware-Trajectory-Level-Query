SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  COUNT(*) AS n,
  ROUND(AVG("Academic stress"), 2) AS avg_academic_stress,
  ROUND(AVG("Financial stress"), 2) AS avg_financial_stress,
  ROUND(AVG("Cumulative GPA (CGPA)"), 2) AS avg_cgpa,
  ROUND(AVG("Satisfaction with studies"), 2) AS avg_study_satisfaction,
  ROUND(AVG("Work/study hours"), 2) AS avg_study_hours,
  ROUND(AVG(Age), 2) AS avg_age
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY suicidal