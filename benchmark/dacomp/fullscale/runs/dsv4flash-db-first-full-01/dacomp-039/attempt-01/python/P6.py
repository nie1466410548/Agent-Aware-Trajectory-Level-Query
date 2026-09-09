import pandas as pd
import numpy as np
from scipy import stats

rows = db.query("SELECT * FROM game_game_level_content_data_ta WHERE strftime('%Y', \"Launch Time\") = '2024'")
df = db.frame(rows)

# 1. Variance decomposition for Churn Rate
n = len(df)
grand_mean = df['Churn Rate'].mean()
ss_total = ((df['Churn Rate'] - grand_mean) ** 2).sum()

# Difficulty level SS
diff_means = df.groupby('Difficulty Level')['Churn Rate'].mean()
ss_diff = sum(df.groupby('Difficulty Level').apply(lambda g: len(g) * (g['Churn Rate'].mean() - grand_mean)**2))

# Level Type SS
type_means = df.groupby('Level Type')['Churn Rate'].mean()
ss_type = sum(df.groupby('Level Type').apply(lambda g: len(g) * (g['Churn Rate'].mean() - grand_mean)**2))

# Cross SS
diff_type_means = df.groupby(['Difficulty Level', 'Level Type'])['Churn Rate'].mean()
ss_cross = 0
for (d, t), grp in df.groupby(['Difficulty Level', 'Level Type']):
    cell_mean = grp['Churn Rate'].mean()
    d_mean = diff_means[d]
    t_mean = type_means[t]
    ss_cross += len(grp) * (cell_mean - d_mean - t_mean + grand_mean)**2

ss_residual = ss_total - ss_diff - ss_type - ss_cross

print("=== Variance Decomposition: Churn Rate ===")
print(f"SS_Total:     {ss_total:.2f}")
print(f"SS_Difficulty: {ss_diff:.2f}  ({ss_diff/ss_total*100:.1f}%)")
print(f"SS_Type:      {ss_type:.2f}  ({ss_type/ss_total*100:.1f}%)")
print(f"SS_Interaction: {ss_cross:.2f}  ({ss_cross/ss_total*100:.1f}%)")
print(f"SS_Residual:  {ss_residual:.2f}  ({ss_residual/ss_total*100:.1f}%)")

# 2. Same for Level Rating
grand_mean_r = df['Level Rating'].mean()
ss_total_r = ((df['Level Rating'] - grand_mean_r) ** 2).sum()

diff_means_r = df.groupby('Difficulty Level')['Level Rating'].mean()
ss_diff_r = sum(df.groupby('Difficulty Level').apply(lambda g: len(g) * (g['Level Rating'].mean() - grand_mean_r)**2))

type_means_r = df.groupby('Level Type')['Level Rating'].mean()
ss_type_r = sum(df.groupby('Level Type').apply(lambda g: len(g) * (g['Level Rating'].mean() - grand_mean_r)**2))

ss_cross_r = 0
for (d, t), grp in df.groupby(['Difficulty Level', 'Level Type']):
    cell_mean = grp['Level Rating'].mean()
    d_mean = diff_means_r[d]
    t_mean = type_means_r[t]
    ss_cross_r += len(grp) * (cell_mean - d_mean - t_mean + grand_mean_r)**2

ss_residual_r = ss_total_r - ss_diff_r - ss_type_r - ss_cross_r

print("\n=== Variance Decomposition: Level Rating ===")
print(f"SS_Total:     {ss_total_r:.2f}")
print(f"SS_Difficulty: {ss_diff_r:.2f}  ({ss_diff_r/ss_total_r*100:.1f}%)")
print(f"SS_Type:      {ss_type_r:.2f}  ({ss_type_r/ss_total_r*100:.1f}%)")
print(f"SS_Interaction: {ss_cross_r:.2f}  ({ss_cross_r/ss_total_r*100:.1f}%)")
print(f"SS_Residual:  {ss_residual_r:.2f}  ({ss_residual_r/ss_total_r*100:.1f}%)")

# 3. Within-difficulty correlation of Reward Value with Churn
print("\n=== Reward Value vs Churn Rate within Difficulty ===")
for diff in ['Easy', 'Normal', 'Hard', 'Hell (Difficulty Level)']:
    sub = df[df['Difficulty Level'] == diff]
    r, p = stats.pearsonr(sub['Reward Value'], sub['Churn Rate'])
    print(f"{diff:25s}: r={r:.4f}, p={p:.4e}, n={len(sub)}")

# 4. Reward Value vs Level Rating within Difficulty
print("\n=== Reward Value vs Level Rating within Difficulty ===")
for diff in ['Easy', 'Normal', 'Hard', 'Hell (Difficulty Level)']:
    sub = df[df['Difficulty Level'] == diff]
    r, p = stats.pearsonr(sub['Reward Value'], sub['Level Rating'])
    print(f"{diff:25s}: r={r:.4f}, p={p:.4e}, n={len(sub)}")

# 5. Are there "outlier" levels (high churn vs rating)?
# For each difficulty, identify levels with churn 1.5 IQR above Q3
print("\n=== Outlier detection (high churn levels) ===")
for diff in ['Easy', 'Normal', 'Hard', 'Hell (Difficulty Level)']:
    sub = df[df['Difficulty Level'] == diff]
    q1 = sub['Churn Rate'].quantile(0.25)
    q3 = sub['Churn Rate'].quantile(0.75)
    iqr = q3 - q1
    threshold = q3 + 1.5 * iqr
    outliers = sub[sub['Churn Rate'] > threshold]
    print(f"{diff:25s}: Q1={q1:.4f}, Q3={q3:.4f}, IQR={iqr:.4f}, threshold={threshold:.4f}, outliers={len(outliers)} ({len(outliers)/len(sub)*100:.1f}%)")