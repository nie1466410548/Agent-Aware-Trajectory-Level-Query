WITH all_rows AS (
  SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" AS units FROM sheet1
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet2
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet3
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet4
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet5
  UNION ALL SELECT "Employee ID", "Gender", "Workstation ID", "Units Produced" FROM sheet6
)
SELECT "Workstation ID", COUNT(DISTINCT "Employee ID") AS emps,
       ROUND(AVG(units),2) AS avg_units, MIN("Gender") AS gender_sample
FROM all_rows
GROUP BY "Workstation ID"
ORDER BY avg_units DESC
LIMIT 15