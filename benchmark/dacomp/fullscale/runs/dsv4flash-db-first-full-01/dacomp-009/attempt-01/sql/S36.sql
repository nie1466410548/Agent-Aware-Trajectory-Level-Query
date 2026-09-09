WITH all_rows AS (
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet1 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet2 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet3 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet4 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet5 UNION ALL
  SELECT "Employee ID", "Employee", "Gender", "Age", "Disciplinary Issue", "Reason for Infraction"
  FROM sheet6
)
SELECT "Reason for Infraction", COUNT(*) AS cnt, "Gender"
FROM all_rows
WHERE "Disciplinary Issue" = 'Yes'
GROUP BY "Reason for Infraction", "Gender"
ORDER BY cnt DESC