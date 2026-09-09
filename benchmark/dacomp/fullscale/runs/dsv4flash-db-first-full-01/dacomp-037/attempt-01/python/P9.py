import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# Prevalence bar chart
sql = """
SELECT
  s."Medical history" AS medhx,
  COUNT(*) AS n,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 130 OR i."Blood Pressure (Diastolic)" >= 85 THEN 1 ELSE 0 END)/COUNT(*) AS pct_elev,
  100.0*SUM(CASE WHEN i."Blood Pressure (Systolic)" >= 140 OR i."Blood Pressure (Diastolic)" >= 90 THEN 1 ELSE 0 END)/COUNT(*) AS pct_high
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
GROUP BY s."Medical history"
"""
df = db.frame(db.query(sql))
groups = ['None', 'Diabetes', 'Hypertension', 'Heart disease']
df = df.set_index('medhx').loc[groups].reset_index()

fig, ax = plt.subplots(figsize=(9, 5))
x = np.arange(len(groups))
w = 0.35
b1 = ax.bar(x - w/2, df['pct_elev'], w, label='Elevated BP (≥130/85)', color='#F9A825', alpha=0.9)
b2 = ax.bar(x + w/2, df['pct_high'], w, label='High BP (≥140/90)', color='#D84315', alpha=0.9)
ax.set_xticks(x)
ax.set_xticklabels(df['medhx'])
ax.set_ylabel('Prevalence (%)')
ax.set_title('Prevalence of Elevated/High Blood Pressure by Medical History', fontweight='bold')
ax.legend()
ax.grid(axis='y', alpha=0.3)
for bars in [b1, b2]:
    for r in bars:
        ax.text(r.get_x() + r.get_width()/2, r.get_height() + 1, f"{r.get_height():.0f}%", ha='center', fontsize=9)
plt.tight_layout()
plt.savefig('/work/bp_prevalence.png', dpi=150)
plt.close()
print("Saved bp_prevalence.png")

# Z-score standardized means table
df_full_sql = """
SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Heart Rate (bpm)" AS hr, i."Respiratory Rate (breaths/min)" AS rr,
  i."Blood Oxygen Saturation (%)" AS spo2, i."Blood Glucose (mmol/L)" AS glucose,
  i."Total Cholesterol (mmol/L)" AS chol, i."Lipoprotein (mmol/L)" AS lipo,
  i."Triglycerides (mmol/L)" AS tg, i."Uric Acid (umol/L)" AS uric,
  i."Blood Urea Nitrogen (mmol/L)" AS bun, i."Alanine Aminotransferase (U/L)" AS alt,
  i."Serum Potassium (mmol/L)" AS k
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
"""
dff = db.frame(db.query(df_full_sql))
inds = ['Age','height','weight','hr','rr','spo2','glucose','chol','lipo','tg','uric','bun','alt','k']
means = dff.groupby('medhx')[inds].mean()
z = (means - means.mean()) / means.std()
print("Z-score standardized means across groups:")
print(z.round(2).to_string())