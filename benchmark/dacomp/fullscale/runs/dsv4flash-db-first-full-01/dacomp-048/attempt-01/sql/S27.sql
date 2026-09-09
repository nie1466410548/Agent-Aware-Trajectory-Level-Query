WITH parsed AS (
  SELECT 
    "Gender Requirement",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT "Gender Requirement", COUNT(*) AS n, 
  ROUND(AVG((salary_min + salary_max)/2.0),1) AS avg_salary,
  ROUND(AVG(salary_min),1) AS avg_min,
  ROUND(AVG(salary_max),1) AS avg_max
FROM parsed
GROUP BY "Gender Requirement"
ORDER BY avg_salary DESC