SELECT 
  "Have you ever had suicidal thoughts?" AS suicidal,
  "Dietary habits",
  COUNT(*) AS n
FROM sheet1 
WHERE "Working professional or student" = 'Student'
GROUP BY suicidal, "Dietary habits"
ORDER BY suicidal, "Dietary habits"