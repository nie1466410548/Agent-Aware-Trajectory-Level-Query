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
print("Shape:", df.shape)
print("Groups:\n", df['medhx'].value_counts())

indicators = ['Age','height','weight','sbp','dbp','hr','rr','spo2','glucose','chol','lipo','tg','uric','bun','alt','k']

# Medians and IQRs
med = df.groupby('medhx')[indicators].median().round(2)
q1 = df.groupby('medhx')[indicators].quantile(0.25).round(2)
q3 = df.groupby('medhx')[indicators].quantile(0.75).round(2)
print("\nMEDIANS:\n", med)
print("\nIQR:\n", (q3-q1).round(2))

# Kruskal-Wallis test across 4 groups
print("\n=== Kruskal-Wallis Test (4 groups) ===")
group_names = ['None','Diabetes','Hypertension','Heart disease']
group_data = {g: df.loc[df['medhx']==g, :] for g in group_names}
for ind in indicators:
    samples = [group_data[g][ind].values for g in group_names]
    H, p = stats.kruskal(*samples)
    print(f"{ind:12s} H={H:8.2f}  p={p:.3e}  {'***' if p<0.001 else ('**' if p<0.01 else '*') if p<0.05 else 'ns'}")

# Compare None vs Any medical history (Mann-Whitney U)
print("\n=== Mann-Whitney U: None vs Any Medical History ===")
df['has_medhx'] = (df['medhx'] != 'None')
for ind in indicators:
    u, p = stats.mannwhitneyu(df.loc[df['has_medhx'], ind], df.loc[~df['has_medhx'], ind], alternative='two-sided')
    none_mean = df.loc[~df['has_medhx'], ind].mean()
    any_mean = df.loc[df['has_medhx'], ind].mean()
    print(f"{ind:12s} U={u:8.0f}  p={p:.3e}  {'***' if p<0.001 else ('**' if p<0.01 else '*') if p<0.05 else 'ns'}  None_mean={none_mean:.2f}  Any_mean={any_mean:.2f}")