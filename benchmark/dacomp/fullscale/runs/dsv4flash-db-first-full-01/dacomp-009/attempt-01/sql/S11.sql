WITH all_emp AS (
  SELECT "Employee ID", "Employee" FROM sheet1
  UNION SELECT "Employee ID", "Employee" FROM sheet2
  UNION SELECT "Employee ID", "Employee" FROM sheet3
  UNION SELECT "Employee ID", "Employee" FROM sheet4
  UNION SELECT "Employee ID", "Employee" FROM sheet5
  UNION SELECT "Employee ID", "Employee" FROM sheet6
)
SELECT COUNT(*) AS total_employees, COUNT(DISTINCT "Employee ID") AS unique_ids FROM all_emp