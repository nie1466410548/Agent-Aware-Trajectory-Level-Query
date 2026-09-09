WITH parsed AS (
  SELECT 
    "Job Title",
    "Work Experience Requirement",
    "Foreign Language Requirement",
    "Age Requirement",
    "Gender Requirement",
    "Employment Type",
    "Company Type",
    "Industry",
    "Work Location",
    "Working Hours",
    "Benefits",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
)
SELECT 
  COUNT(*) AS n,
  SUM(CASE WHEN salary_min IS NULL OR salary_max IS NULL THEN 1 ELSE 0 END) AS parse_fail,
  ROUND(AVG(salary_min),1) AS avg_min,
  ROUND(AVG(salary_max),1) AS avg_max,
  ROUND(AVG((salary_min + salary_max) / 2.0),1) AS avg_mid,
  MIN(salary_min) AS min_salary,
  MAX(salary_max) AS max_salary
FROM parsed