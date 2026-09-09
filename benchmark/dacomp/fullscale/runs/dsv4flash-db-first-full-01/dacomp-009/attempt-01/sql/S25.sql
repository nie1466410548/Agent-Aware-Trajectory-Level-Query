SELECT "Gender", COUNT(DISTINCT "Employee ID") AS cnt FROM (
  SELECT "Employee ID", "Gender" FROM sheet1 UNION
  SELECT "Employee ID", "Gender" FROM sheet2 UNION
  SELECT "Employee ID", "Gender" FROM sheet3 UNION
  SELECT "Employee ID", "Gender" FROM sheet4 UNION
  SELECT "Employee ID", "Gender" FROM sheet5 UNION
  SELECT "Employee ID", "Gender" FROM sheet6
) GROUP BY "Gender"