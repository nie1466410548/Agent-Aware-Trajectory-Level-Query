import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import stats

# Fetch all numeric indicators
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
df = db.frame(db.query(sql))

indicators = ['Age','height','weight','sbp','dbp','hr','rr','spo2','glucose','chol','lipo','tg','uric','bun','alt','k']
groups = ['Diabetes','Hypertension','Heart disease']
none_data = df[df['medhx']=='None']

def cohens_d(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na-1)*a.std(ddof=1)**2 + (nb-1)*b.std(ddof=1)**2) / (na+nb-2))
    return (a.mean()-b.mean())/sp if sp != 0 else 0.0

# Build effect size matrix
d_matrix = np.zeros((len(groups), len(indicators)))
p_matrix = np.zeros((len(groups), len(indicators)))
for i, g in enumerate(groups):
    gdata = df[df['medhx']==g]
    for j, ind in enumerate(indicators):
        d_matrix[i,j] = cohens_d(gdata[ind].values, none_data[ind].values)
        _, p = stats.mannwhitneyu(gdata[ind].values, none_data[ind].values, alternative='two-sided')
        p_matrix[i,j] = p

# Plot heatmap
fig, ax = plt.subplots(figsize=(14, 5))
im = ax.imshow(d_matrix, cmap='RdBu_r', vmin=-1.0, vmax=1.0, aspect='auto')

ax.set_xticks(range(len(indicators)))
ax.set_xticklabels(indicators, rotation=45, ha='right', fontsize=10)
ax.set_yticks(range(len(groups)))
ax.set_yticklabels(groups, fontsize=10)

# Annotate cells
for i in range(len(groups)):
    for j in range(len(indicators)):
        d_val = d_matrix[i,j]
        p_val = p_matrix[i,j]
        sig = '***' if p_val<0.001 else ('**' if p_val<0.01 else '*') if p_val<0.05 else ''
        txt = f'{d_val:.2f}\n{sig}'
        color = 'white' if abs(d_val) > 0.5 else 'black'
        ax.text(j, i, txt, ha='center', va='center', fontsize=8, color=color)

ax.set_title("Cohen's d Effect Size vs. 'None' Medical History Group\n(negative = lower than None, positive = higher than None)", fontsize=11)
plt.colorbar(im, ax=ax, label="Cohen's d")
plt.tight_layout()
plt.savefig('/work/effect_size_heatmap.png', dpi=150)
plt.close()
print("Saved effect_size_heatmap.png")

# Also check gender-specific weight differences
print("\n=== Weight by medical history AND gender ===")
sql2 = """
SELECT s."Medical history" AS medhx, i.Gender, i."Weight (kg)" AS weight
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
"""
df2 = db.frame(db.query(sql2))
print(df2.groupby(['medhx','Gender'])['weight'].agg(['mean','std','count']).round(2))