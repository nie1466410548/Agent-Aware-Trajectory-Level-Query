import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Use db.frame to get proper DataFrame
df_t = db.frame(db.query("""
WITH case_outcome AS (
  SELECT "Case ID",
    MAX(CASE WHEN "Outcome (Cured/Improved/Deceased)" = 'Deceased' THEN 1 ELSE 0 END) AS is_deceased
  FROM clinical_manifestations GROUP BY "Case ID"
)
SELECT CASE WHEN is_deceased=1 THEN 'Deceased' ELSE 'Recovered' END AS grp,
  "Highest Body Temperature (°C)" AS temp
FROM clinical_manifestations cm JOIN case_outcome co ON cm."Case ID"=co."Case ID"
"""))

print(df_t.head())
print(df_t.dtypes)
print(df_t['grp'].value_counts())