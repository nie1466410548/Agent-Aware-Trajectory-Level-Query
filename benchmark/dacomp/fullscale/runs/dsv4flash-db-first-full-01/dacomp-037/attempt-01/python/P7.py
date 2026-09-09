import pandas as pd
import numpy as np

# Null checks via SQL-like aggregation in Python (small aggregated result)
sql = """
SELECT s."Medical history" AS medhx, i.Gender,
  ROUND(AVG(i."Blood Pressure (Systolic)"),2) AS sbp_mean,
  ROUND(AVG(i."Blood Pressure (Diastolic)"),2) AS dbp_mean
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history", i.Gender
ORDER BY s."Medical history", i.Gender
"""
df = db.frame(db.query(sql))
print("BP by medhx & gender:\n", df.to_string(index=False))

# Check for any nulls across all columns
sql2 = "SELECT COUNT(*) AS total FROM health_checkup_indicators"
total = db.frame(db.query(sql2)).iloc[0,0]
sql3 = """
SELECT
  SUM(CASE WHEN Age IS NULL THEN 1 ELSE 0 END) AS age_null,
  SUM(CASE WHEN "Weight (kg)" IS NULL THEN 1 ELSE 0 END) AS weight_null,
  SUM(CASE WHEN "Blood Pressure (Systolic)" IS NULL THEN 1 ELSE 0 END) AS sbp_null,
  SUM(CASE WHEN "Blood Glucose (mmol/L)" IS NULL THEN 1 ELSE 0 END) AS glu_null
FROM health_checkup_indicators
"""
nulls = db.frame(db.query(sql3))
print("Null counts (indicators):", nulls.to_dict('records'))
sql4 = """
SELECT
  SUM(CASE WHEN "Medical history" IS NULL THEN 1 ELSE 0 END) AS mhx_null,
  SUM(CASE WHEN "Health status" IS NULL THEN 1 ELSE 0 END) AS hs_null,
  SUM(CASE WHEN ID IS NULL THEN 1 ELSE 0 END) AS id_null
FROM health_status
"""
nulls2 = db.frame(db.query(sql4))
print("Null counts (status):", nulls2.to_dict('records'))
print("Total rows:", total)