SELECT DISTINCT "Employee ID", "Employee", "Base Salary", "Company Accommodation"
FROM (
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet1
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet2
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet3
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet4
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet5
  UNION ALL
  SELECT "Employee ID", "Employee", "Base Salary", "Company Accommodation" FROM sheet6
)
GROUP BY "Employee ID", "Employee"
ORDER BY "Base Salary" DESC