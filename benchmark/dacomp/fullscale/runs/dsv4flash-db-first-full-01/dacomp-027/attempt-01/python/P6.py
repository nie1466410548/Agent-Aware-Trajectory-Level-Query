import pandas as pd, numpy as np
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('whitegrid')

# Get review dates directly
res = db.query("SELECT c.\"Secincident Count\", c.\"nextreviewdate\" FROM coordination_and_evaluation c")
review_df = db.frame(res)
review_df['nextreviewdate'] = pd.to_datetime(review_df['nextreviewdate'], errors='coerce')
review_df['days_till_review'] = (pd.Timestamp('2025-09-08') - review_df['nextreviewdate']).dt.days
review_df['sec_group'] = pd.cut(review_df['Secincident Count'], bins=[-1, 32, 65, 100], 
                                  labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
print("=== Days till next review (negative = overdue) ===")
print(review_df.groupby('sec_group')['days_till_review'].agg(['mean','median','min','max']).round(1))

# Proportion of overdue reviews
review_df['overdue'] = review_df['days_till_review'] < 0
print("\n=== Overdue reviews proportion ===")
print(review_df.groupby('sec_group')['overdue'].mean().round(3))

# Chi-square test for overdue status vs sec_group
ct = pd.crosstab(review_df['sec_group'], review_df['overdue'])
chi2, p, _, _ = stats.chi2_contingency(ct)
print(f"\nChi-square: overdue vs sec_group -> chi2={chi2:.2f}, p={p:.4f}")
print(ct)

# Also check contingencyplanstage by sec_group
res2 = db.query("SELECT c.\"Secincident Count\", c.\"contingencyplanstage\" FROM coordination_and_evaluation c")
contingency = db.frame(res2)
contingency['sec_group'] = pd.cut(contingency['Secincident Count'], bins=[-1, 32, 65, 100], 
                                  labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
print("\n=== Contingency Plan Stage by sec_group ===")
ct2 = pd.crosstab(contingency['sec_group'], contingency['contingencyplanstage'])
chi2_2, p_2, _, _ = stats.chi2_contingency(ct2)
print(f"Chi2={chi2_2:.2f}, p={p_2:.4f}")
print(ct2)

# Check operation phase by sec group (from cat_df)
cat_df = pd.read_csv('/work/cat_joined.csv')
cat_df['sec_group'] = pd.cut(cat_df['Secincident Count'], bins=[-1, 32, 65, 100], 
                              labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
# Response Phase vs sec group
print("\n=== Response Phase by sec_group ===")
ct3 = pd.crosstab(cat_df['sec_group'], cat_df['Response Phase'])
chi2_3, p_3, _, _ = stats.chi2_contingency(ct3)
print(f"Chi2={chi2_3:.2f}, p={p_3:.4f}")
print(ct3)

# Check Operation Status vs Disaster Level (from main df)
df = pd.read_csv('/work/full_joined.csv')
df['sec_group'] = pd.cut(df['Secincident Count'], bins=[-1, 32, 65, 100], 
                          labels=['Low (0-32)','Medium (33-65)','High (66-100)'])
print("\n=== Operation Status by Disaster Level ===")
ct4 = pd.crosstab(df['Disaster Level'], df['Operation Status'], normalize='index').round(3)
print(ct4)

# Resource Allocation Status by sec group
print("\n=== Resource Allocation Status by sec group ===")
ct5 = pd.crosstab(cat_df['sec_group'], cat_df['Resource Allocation Status'], normalize='index').round(3)
print(ct5)

# Insurance scope by sec group
print("\n=== Insurance Scope by sec group ===")
ct6 = pd.crosstab(cat_df['sec_group'], cat_df['insurancescope'], normalize='index').round(3)
print(ct6)

# Section: environmental impact by disaster level (for the report)
print("\n=== Environmental Impact Rate by Disaster Level (normalized) ===")
ct7 = pd.crosstab(df['Disaster Level'], df['Environmental Impact Rate'], normalize='index').round(3)
print(ct7)

print("\n=== All figures already saved: fig1, fig2, fig3, fig4 ===")