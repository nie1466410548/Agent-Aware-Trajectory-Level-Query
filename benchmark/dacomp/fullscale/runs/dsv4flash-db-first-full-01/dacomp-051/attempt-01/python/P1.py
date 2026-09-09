import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Get task data for slow vs fast cohorts
result = db.query("""
SELECT t.*,
  CASE WHEN u.avg_close_time_assigned_days > (SELECT 1.5*AVG(avg_close_time_assigned_days) FROM asana__user) THEN 'SLOW' ELSE 'FAST' END AS cohort
FROM asana__task_lifecycle_analysis t
JOIN asana__user u ON CAST(t.assignee_user_id AS TEXT) = u.user_id
WHERE t.is_valid_record=1
""")
df = db.frame(result)
print(f"Total rows: {len(df)}")
print(f"Cohort counts: {df['cohort'].value_counts().to_dict()}")
print(f"\nColumns: {list(df.columns)}")

# Distribution comparison
fig, axes = plt.subplots(2, 3, figsize=(15, 10))

# Complexity score distribution
for i, col in enumerate(['complexity_score', 'urgency_score', 'project_health_score']):
    ax = axes[0, i]
    for cohort in ['FAST', 'SLOW']:
        data = df[df['cohort']==cohort][col].dropna()
        ax.hist(data, bins=20, alpha=0.6, label=f'{cohort} (n={len(data)})')
    ax.set_xlabel(col)
    ax.set_ylabel('Frequency')
    ax.legend()
    ax.set_title(f'{col} Distribution by Cohort')

# Box plots
for i, col in enumerate(['complexity_score', 'urgency_score', 'project_health_score']):
    ax = axes[1, i]
    df.boxplot(column=col, by='cohort', ax=ax)
    ax.set_title(f'{col} by Cohort')
    ax.set_xlabel('')

plt.suptitle('Task Distribution Comparison: Slow vs Fast Users', fontsize=14)
plt.tight_layout()
plt.savefig('/work/cohort_distributions.png', dpi=100)
print("Saved cohort_distributions.png")

# Statistical tests
print("\n=== Statistical Tests ===")
for col in ['complexity_score', 'urgency_score', 'project_health_score']:
    slow = df[df['cohort']=='SLOW'][col].dropna()
    fast = df[df['cohort']=='FAST'][col].dropna()
    t_stat, p_val = stats.ttest_ind(slow, fast, equal_var=False)
    print(f"{col}: SLOW mean={slow.mean():.3f}, FAST mean={fast.mean():.3f}, t={t_stat:.3f}, p={p_val:.4f}")

# Chi-square test for complexity_execution_match
print("\n=== Complexity Execution Match ===")
ct = pd.crosstab(df['cohort'], df['complexity_execution_match'])
print(ct)
chi2, p, dof, expected = stats.chi2_contingency(ct)
print(f"Chi2={chi2:.2f}, p={p:.4f}")

# Chi-square for lifecycle_efficiency_category
print("\n=== Lifecycle Efficiency Category ===")
ct2 = pd.crosstab(df['cohort'], df['lifecycle_efficiency_category'])
print(ct2)
chi2, p = stats.chi2_contingency(ct2)[:2]
print(f"Chi2={chi2:.2f}, p={p:.4f}")

# Chi-square for improvement_opportunities
print("\n=== Improvement Opportunities ===")
ct3 = pd.crosstab(df['cohort'], df['improvement_opportunities'])
print(ct3)
chi2, p = stats.chi2_contingency(ct3)[:2]
print(f"Chi2={chi2:.2f}, p={p:.4f}")