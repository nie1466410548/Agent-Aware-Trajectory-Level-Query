import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

sql = """
SELECT s."Medical history" AS medhx,
  i.Age, i."Height (cm)" AS height, i."Weight (kg)" AS weight,
  i."Blood Pressure (Systolic)" AS sbp, i."Blood Pressure (Diastolic)" AS dbp,
  i."Lipoprotein (mmol/L)" AS lipo
FROM health_status s JOIN health_checkup_indicators i ON s.ID = i.ID
"""
df = db.frame(db.query(sql))

# Set style
plt.style.use('default')
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. SBP boxplot
groups = ['None', 'Diabetes', 'Hypertension', 'Heart disease']
data_sbp = [df.loc[df['medhx']==g, 'sbp'].values for g in groups]
bp1 = axes[0,0].boxplot(data_sbp, labels=groups, patch_artist=True, widths=0.6)
colors = ['#4CAF50','#FF9800','#F44336','#2196F3']
for patch, col in zip(bp1['boxes'], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.7)
axes[0,0].set_title('Systolic Blood Pressure by Medical History', fontsize=12, fontweight='bold')
axes[0,0].set_ylabel('SBP (mmHg)')
axes[0,0].grid(axis='y', alpha=0.3)

# 2. DBP boxplot
data_dbp = [df.loc[df['medhx']==g, 'dbp'].values for g in groups]
bp2 = axes[0,1].boxplot(data_dbp, labels=groups, patch_artist=True, widths=0.6)
for patch, col in zip(bp2['boxes'], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.7)
axes[0,1].set_title('Diastolic Blood Pressure by Medical History', fontsize=12, fontweight='bold')
axes[0,1].set_ylabel('DBP (mmHg)')
axes[0,1].grid(axis='y', alpha=0.3)

# 3. Weight boxplot
data_wt = [df.loc[df['medhx']==g, 'weight'].values for g in groups]
bp3 = axes[1,0].boxplot(data_wt, labels=groups, patch_artist=True, widths=0.6)
for patch, col in zip(bp3['boxes'], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.7)
axes[1,0].set_title('Weight by Medical History', fontsize=12, fontweight='bold')
axes[1,0].set_ylabel('Weight (kg)')
axes[1,0].grid(axis='y', alpha=0.3)

# 4. Lipoprotein boxplot
data_lipo = [df.loc[df['medhx']==g, 'lipo'].values for g in groups]
bp4 = axes[1,1].boxplot(data_lipo, labels=groups, patch_artist=True, widths=0.6)
for patch, col in zip(bp4['boxes'], colors):
    patch.set_facecolor(col)
    patch.set_alpha(0.7)
axes[1,1].set_title('Lipoprotein by Medical History', fontsize=12, fontweight='bold')
axes[1,1].set_ylabel('Lipoprotein (mmol/L)')
axes[1,1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('/work/boxplots_key_indicators.png', dpi=150)
plt.close()
print("Saved boxplots_key_indicators.png")

# Create a heatmap of mean differences (None as baseline)
print("\n=== Mean difference from None group ===")
baseline = df[df['medhx']=='None'][['weight','sbp','dbp','lipo','height']].mean()
for g in ['Diabetes','Hypertension','Heart disease']:
    diff = df[df['medhx']==g][['weight','sbp','dbp','lipo','height']].mean() - baseline
    print(f"{g:12s}: {diff.round(2).to_dict()}")