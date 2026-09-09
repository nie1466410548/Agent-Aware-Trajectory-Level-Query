import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sql = """
SELECT s."Medical history" AS medhx,
  i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Lipoprotein (mmol/L)" AS lipo
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
"""
df = db.frame(db.query(sql))
groups = ['None', 'Diabetes', 'Hypertension', 'Heart disease']
colors = ['#4CAF50','#FF9800','#F44336','#2196F3']

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
plots = [
    (axes[0,0], 'sbp', 'Systolic Blood Pressure by Medical History', 'SBP (mmHg)'),
    (axes[0,1], 'dbp', 'Diastolic Blood Pressure by Medical History', 'DBP (mmHg)'),
    (axes[1,0], 'weight', 'Weight by Medical History', 'Weight (kg)'),
    (axes[1,1], 'lipo', 'Lipoprotein by Medical History', 'Lipoprotein (mmol/L)'),
]
for ax, col, title, ylab in plots:
    data = [df.loc[df['medhx']==g, col].values for g in groups]
    bp = ax.boxplot(data, tick_labels=groups, patch_artist=True, widths=0.6)
    for patch, c in zip(bp['boxes'], colors):
        patch.set_facecolor(c)
        patch.set_alpha(0.7)
    ax.set_title(title, fontsize=12, fontweight='bold')
    ax.set_ylabel(ylab)
    ax.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/boxplots_key_indicators.png', dpi=150)
plt.close()
print("Saved boxplots_key_indicators.png")

# Mean difference from None baseline
print("\n=== Mean difference from None group ===")
base = df[df['medhx']=='None'][['weight','sbp','dbp','lipo']].mean()
for g in ['Diabetes','Hypertension','Heart disease']:
    diff = df[df['medhx']==g][['weight','sbp','dbp','lipo']].mean() - base
    print(f"{g:12s}: {diff.round(2).to_dict()}")