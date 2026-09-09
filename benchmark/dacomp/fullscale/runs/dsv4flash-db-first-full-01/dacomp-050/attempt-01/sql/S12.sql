SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  "Sleep duration",
  COUNT(*) AS n
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY suicidal, "Sleep duration"
ORDER BY suicidal, "Sleep duration"