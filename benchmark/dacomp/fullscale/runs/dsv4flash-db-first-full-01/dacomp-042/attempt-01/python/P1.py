import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import chi2_contingency

# Load the main cross-tabulation data
# Barrier × age_group cross-tab
barrier_age = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier
ORDER BY age_group, barrier
""")
df_ba = db.frame(barrier_age)
print("Barrier × Age Group:")
print(df_ba)

# Create contingency table
ct_ba = df_ba.pivot(index='age_group', columns='barrier', values='n').fillna(0).astype(int)
print("\nContingency table Barrier × Age Group:")
print(ct_ba)

chi2, p, dof, expected = chi2_contingency(ct_ba)
print(f"\nChi-square test Barrier × Age Group:")
print(f"Chi2 = {chi2:.4f}, p = {p:.6f}, df = {dof}")

# Symptom improvement × age_group
imp_age = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, improvement
ORDER BY age_group, improvement
""")
df_ia = db.frame(imp_age)
print("\n\nImprovement × Age Group:")
print(df_ia)

ct_ia = df_ia.pivot(index='age_group', columns='improvement', values='n').fillna(0).astype(int)
print("\nContingency table Improvement × Age Group:")
print(ct_ia)

chi2_i, p_i, dof_i, expected_i = chi2_contingency(ct_ia)
print(f"\nChi-square test Improvement × Age Group:")
print(f"Chi2 = {chi2_i:.4f}, p = {p_i:.6f}, df = {dof_i}")

# Full 3-way: barrier × improvement within each age group
full = db.query("""
SELECT
  CASE WHEN p.Age BETWEEN 18 AND 44 THEN 'young_18-44'
       WHEN p.Age BETWEEN 45 AND 59 THEN 'middle_45-59'
       ELSE 'older_60+' END AS age_group,
  e."Treatment Barriers" AS barrier,
  o."Symptom improvement" AS improvement,
  COUNT(*) AS n
FROM treatmentoutcomes o
JOIN treatmentbasics tb ON tb."Treatment ID" = o."Treatment reference"
JOIN encounters e ON e."Visit Record Number" = tb."Visit Reference"
JOIN patients p ON e."Patient Reference Number" = p."Patient number"
GROUP BY age_group, barrier, improvement
ORDER BY age_group, barrier, improvement
""")
df_full = db.frame(full)
print("\n\nFull 3-way cross-tab:")
print(df_full)

# For each age group, test barrier × improvement association
for age_grp in ['young_18-44', 'middle_45-59', 'older_60+']:
    sub = df_full[df_full['age_group'] == age_grp]
    ct = sub.pivot(index='barrier', columns='improvement', values='n').fillna(0).astype(int)
    print(f"\n--- {age_grp} ---")
    print(ct)
    if ct.shape[0] > 1 and ct.shape[1] > 1:
        chi2_s, p_s, dof_s, exp_s = chi2_contingency(ct)
        print(f"Chi2 = {chi2_s:.4f}, p = {p_s:.6f}, df = {dof_s}")
    else:
        print("Insufficient dimensions for chi-square")

# Compute proportions of improvement by barrier within each age group
print("\n\n=== Proportions of improvement by barrier within each age group ===")
for age_grp in ['young_18-44', 'middle_45-59', 'older_60+']:
    sub = df_full[df_full['age_group'] == age_grp].copy()
    total = sub.groupby('barrier')['n'].transform('sum')
    sub['pct'] = sub['n'] / total * 100
    print(f"\n{age_grp}:")
    print(sub.to_string(index=False))

# Also compute the "Minimal improvement rate" as a key metric for each barrier
print("\n\n=== Minimal improvement rate by barrier and age group ===")
minimal = df_full[df_full['improvement'] == 'Minimal'].copy()
minimal = minimal[['age_group', 'barrier', 'n']].rename(columns={'n': 'minimal_n'})
total_b = df_full.groupby(['age_group', 'barrier'])['n'].sum().reset_index().rename(columns={'n': 'total_n'})
merged = pd.merge(minimal, total_b, on=['age_group', 'barrier'])
merged['minimal_rate'] = merged['minimal_n'] / merged['total_n'] * 100
print(merged.to_string(index=False))