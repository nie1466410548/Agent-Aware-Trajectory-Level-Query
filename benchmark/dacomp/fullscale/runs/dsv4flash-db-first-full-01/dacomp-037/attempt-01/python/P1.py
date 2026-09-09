
import pandas as pd
import numpy as np
from scipy import stats

# Retrieve only needed columns for statistical analysis
sql = """
SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
"""
res = db.query(sql)
df = db.frame(res)
print(df.shape)
print(df['medhx'].value_counts())

indicators = ['Age','height','weight','sbp','dbp','hr','rr','spo2','glucose','chol','lipo','tg','uric','bun','alt','k']

# Medians and IQRs by group
med = df.groupby('medhx')[indicators].median().round(2)
q1 = df.groupby('medhx')[indicators].quantile(0.25).round(2)
q3 = df.groupby('medhx')[indicators].quantile(0.75).round(2)
print("MEDIANS:\n", med)
print("\nIQR (Q3-Q1):\n", (q3-q1).round(2))

# Kruskal-Wallis across the 4 groups for each indicator
print("\nKruskal-Wallis across 4 medical-history groups:")
groups = {g: df.loc[df['medhx']==g, ind].values for g in df['medhx'].unique()}
for ind in indicators:
    data = [groups[g] for g in ['None','Diabetes','Hypertension','Heart disease']]
    H, p = stats.kruskal(*data)
    print(f"{ind:8s} H={H:8.2f} p={p:.3e} {'SIG' if p<0.001 else ''}")
