WITH parsed AS (
  SELECT 
    "Employment Type",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Employment Type", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Employment Type"
ORDER BY avg_salary DESC