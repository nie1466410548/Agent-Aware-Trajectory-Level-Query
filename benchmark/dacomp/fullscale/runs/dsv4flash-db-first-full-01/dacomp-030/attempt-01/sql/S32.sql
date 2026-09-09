SELECT "Outlet Type",
  CAST(REPLACE("Qualification Rate", '%', '') AS REAL) AS qual_pct
FROM "point_of_sale_(pos)_information"
WHERE "Qualification Rate" IS NOT NULL AND "Qualification Rate" != ''
LIMIT 20