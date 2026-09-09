import pandas as pd
import numpy as np
from scipy import stats

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

key = ['weight','sbp','dbp','lipo','height']
groups = ['None','Diabetes','Hypertension','Heart disease']
gdata = {g: df.loc[df['medhx']==g] for g in groups}

def cohens_d(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na-1)*a.std(ddof=1)**2 + (nb-1)*b.std(ddof=1)**2) / (na+nb-2))
    return (a.mean()-b.mean())/sp

# Pairwise comparisons (Mann-Whitney U with rank-biserial r)
print("=== Pairwise comparisons: significant indicators ===")
for ind in key:
    print(f"\n--- {ind} ---")
    for gi in range(len(groups)):
        for gj in range(gi+1, len(groups)):
            a = gdata[groups[gi]][ind].values
            b = gdata[groups[gj]][ind].values
            u, p = stats.mannwhitneyu(a, b, alternative='two-sided')
            d = cohens_d(a, b)
            rb = 1 - (2*u)/(len(a)*len(b))
            sig = '***' if p<0.001 else ('**' if p<0.01 else '*') if p<0.05 else 'ns'
            print(f"{groups[gi]:12s} vs {groups[gj]:12s} p={p:.3e} {sig}  Cohen_d={d:+.2f}  r_rankbiserial={rb:+.2f}")

# Descriptive means table for key indicators
print("\n=== Group means (key indicators) ===")
for ind in key:
    print(ind, {g: round(gdata[g][ind].mean(),2) for g in groups})