import sqlite3
# Read the first row as a dict to see exact column names
result = db.query("SELECT * FROM light_and_radiation_readings LIMIT 1")
print("Light columns:", result['executions'][0]['columns'])
result2 = db.query("SELECT * FROM surface_and_physical_readings LIMIT 1")
print("Surface columns:", result2['executions'][0]['columns'])