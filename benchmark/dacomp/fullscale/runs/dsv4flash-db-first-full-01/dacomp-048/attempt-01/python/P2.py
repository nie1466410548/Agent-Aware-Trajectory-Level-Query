import json

# Check the format of the result
result = db.query("""
  SELECT 
    "Job Title", "Work Experience Requirement", "Foreign Language Requirement",
    "Gender Requirement", "Company Type", "Industry", "Work Location",
    "Working Hours", "Benefits", "Salary Range",
    CAST(REPLACE(SUBSTR("Salary Range", 1, INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_min,
    CAST(REPLACE(SUBSTR("Salary Range", INSTR("Salary Range", '-') + 1, INSTR("Salary Range", ' ') - INSTR("Salary Range", '-') - 1), ',', '') AS INTEGER) AS salary_max
  FROM sheet1 
  WHERE "Education Requirement" = 'Vocational school or above' 
    AND "Salary Range" IS NOT NULL AND "Salary Range" != ''
""")

print(type(result))
print(result.keys())
print(type(result['executions']))
print(len(result['executions']))
exec0 = result['executions'][0]
print(exec0.keys())
print("columns:", exec0['columns'])
print("row_count:", exec0['row_count'])
print("result_file:", exec0['result_file'])
print("result_complete type:", type(exec0['result_complete']))
print("result_complete len:", len(exec0['result_complete']))
print("First 3:", exec0['result_complete'][:3])