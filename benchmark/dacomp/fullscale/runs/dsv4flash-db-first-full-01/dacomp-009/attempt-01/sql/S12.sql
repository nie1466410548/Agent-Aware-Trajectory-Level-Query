SELECT Team, COUNT(DISTINCT "Employee ID") AS emps FROM (
  SELECT "Employee ID", Team FROM sheet1 UNION ALL
  SELECT "Employee ID", Team FROM sheet2 UNION ALL
  SELECT "Employee ID", Team FROM sheet3 UNION ALL
  SELECT "Employee ID", Team FROM sheet4 UNION ALL
  SELECT "Employee ID", Team FROM sheet5 UNION ALL
  SELECT "Employee ID", Team FROM sheet6
) GROUP BY Team ORDER BY emps DESC