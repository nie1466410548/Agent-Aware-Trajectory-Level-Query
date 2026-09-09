SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  Gender, Age, "Academic stress", "Financial stress", "Satisfaction with studies",
  "Work/study hours", "Sleep duration", "Dietary habits", "Family history of mental illness"
FROM sheet1 
WHERE "Working professional or student" = 'Student'
  AND "Dietary habits" IN ('Healthy','Moderate','Unhealthy')
  AND "Sleep duration" IS NOT NULL
  AND "Academic stress" IS NOT NULL
  AND "Financial stress" IS NOT NULL