SELECT 
  "Salary Range",
  CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min_raw,
  CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max_raw
FROM sheet1 
WHERE "Education Requirement" = 'Vocational school or above' 
  AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
LIMIT 20