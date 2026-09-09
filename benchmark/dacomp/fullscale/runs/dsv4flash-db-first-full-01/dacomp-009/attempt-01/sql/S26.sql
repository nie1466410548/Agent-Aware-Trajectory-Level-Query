SELECT Team, COUNT(DISTINCT "Employee ID") AS cnt FROM (
  SELECT "Employee ID", Team FROM sheet1 UNION
  SELECT "Employee ID", Team FROM sheet2 UNION
  SELECT "Employee ID", Team FROM sheet3 UNION
  SELECT "Employee ID", Team FROM sheet4 UNION
  SELECT "Employee ID", Team FROM sheet5 UNION
  SELECT "Employee ID", Team FROM sheet6
) GROUP BY Team