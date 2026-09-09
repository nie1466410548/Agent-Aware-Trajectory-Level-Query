WITH all_rows AS (
  SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" AS units FROM sheet1
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet2
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet3
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet4
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet5
  UNION ALL SELECT "Employee ID", "Gender", Team, "Workstation ID", "Units Produced" FROM sheet6
)
SELECT Team, "Gender", COUNT(DISTINCT "Employee ID") AS emps, ROUND(AVG(units),2) AS avg_units_per_day
FROM all_rows
GROUP BY Team, "Gender"
ORDER BY Team, "Gender"