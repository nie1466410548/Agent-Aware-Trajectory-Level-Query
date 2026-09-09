WITH parsed AS (
  SELECT 
    "Work Experience Requirement",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Work Experience Requirement", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary
FROM parsed
GROUP BY "Work Experience Requirement"
ORDER BY n DESC