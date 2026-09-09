import json

# Check first few lines
with open('/results/S36.rows.jsonl', 'r') as f:
    for i, line in enumerate(f):
        if i < 3:
            data = json.loads(line)
            print(f"Row {i}: type={type(data)}, data={data}")
        else:
            break

# Also check what columns are
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
  LIMIT 3
""")
print("Columns:", result['executions'][0]['columns'])