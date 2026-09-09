SELECT COUNT(*) AS multi_type_owners FROM (
  SELECT "Task Owner" FROM sheet1 GROUP BY "Task Owner" HAVING COUNT(DISTINCT "Task Type") > 1
)