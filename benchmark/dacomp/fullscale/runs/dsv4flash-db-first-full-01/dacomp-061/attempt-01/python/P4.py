import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Check regression_ratio distribution for the two project groups
reg_fast = db.frame(db.query("""
    SELECT 
        regression_ratio,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio
"""))
print("=== Regression ratio distribution for FAST projects ===")
print(reg_fast.to_string())
total_fast = reg_fast['cnt'].sum()
for _, row in reg_fast.iterrows():
    print(f"  regression_ratio={row['regression_ratio']}: {row['cnt']} ({row['cnt']/total_fast*100:.1f}%)")

reg_slow = db.frame(db.query("""
    SELECT 
        regression_ratio,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio
"""))
print("\n=== Regression ratio distribution for OTHER projects ===")
total_slow = reg_slow['cnt'].sum()
for _, row in reg_slow.iterrows():
    print(f"  regression_ratio={row['regression_ratio']}: {row['cnt']} ({row['cnt']/total_slow*100:.1f}%)")

# Chi-squared test for independence
from scipy.stats import chi2_contingency

# Build contingency table
fast_dict = {r['regression_ratio']: r['cnt'] for _, r in reg_fast.iterrows()}
slow_dict = {r['regression_ratio']: r['cnt'] for _, r in reg_slow.iterrows()}
all_ratios = sorted(set(list(fast_dict.keys()) + list(slow_dict.keys())))

cont_table = np.array([[fast_dict.get(r, 0) for r in all_ratios],
                       [slow_dict.get(r, 0) for r in all_ratios]])
chi2, p_val, dof, expected = chi2_contingency(cont_table)
print(f"\nChi-squared test: chi2={chi2:.2f}, p={p_val:.4f}")

# Create a bar chart comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
labels = [f'Ratio={r}' for r in all_ratios]
colors_pie = ['#4CAF50', '#FFC107', '#F44336'][:len(all_ratios)]

# Fast projects
fast_vals = [fast_dict.get(r, 0) for r in all_ratios]
axes[0].pie(fast_vals, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
axes[0].set_title('Fast Projects (avg_close < 15d)\nRegression Ratio Distribution')

# Other projects
slow_vals = [slow_dict.get(r, 0) for r in all_ratios]
axes[1].pie(slow_vals, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
axes[1].set_title('Other Projects (avg_close >= 15d)\nRegression Ratio Distribution')

plt.tight_layout()
plt.savefig('/work/regression_distribution.png', dpi=150)
plt.close()

# Now analyze specific risk patterns
print("\n\n=== Risk Score Profile Comparison ===")
risk_profile = db.frame(db.query("""
    SELECT 
        CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END as project_group,
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity
    FROM jira__issue_intelligence_analytics
    GROUP BY project_group
"""))
print(risk_profile.to_string())

# Risk score bar chart
fig, ax = plt.subplots(figsize=(12, 6))
risk_cols = ['avg_age_risk', 'avg_process_risk', 'avg_complexity_risk', 'avg_engagement_risk', 
             'avg_assignment_risk', 'avg_deviation_risk', 'avg_total_risk', 'avg_opportunity']
x = np.arange(len(risk_cols))
width = 0.35
fast_risks = [risk_profile[risk_profile['project_group']=='Fast Projects'][c].values[0] for c in risk_cols]
other_risks = [risk_profile[risk_profile['project_group']=='Other Projects'][c].values[0] for c in risk_cols]
ax.bar(x - width/2, fast_risks, width, label='Fast Projects', color='coral', alpha=0.8)
ax.bar(x + width/2, other_risks, width, label='Other Projects', color='steelblue', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(['Age Risk', 'Process Risk', 'Complexity Risk', 'Engagement Risk', 
                    'Assignment Risk', 'Deviation Risk', 'Total Risk', 'Opportunity'], rotation=20)
ax.set_ylabel('Average Score')
ax.set_title('Risk & Opportunity Profile: Fast vs Other Projects')
ax.legend()
plt.tight_layout()
plt.savefig('/work/risk_profile_comparison.png', dpi=150)
plt.close()

# Check the lifecycle_quality_score distribution
print("\n\n=== Lifecycle Quality Score Distribution ===")
lqs_all = db.frame(db.query("""
    SELECT lifecycle_quality_score, COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY lifecycle_quality_score
    ORDER BY lifecycle_quality_score
"""))
print(lqs_all.to_string())

# Per project group LQS
lqs_detail = db.frame(db.query("""
    SELECT 
        CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END as project_group,
        lifecycle_quality_score,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY project_group, lifecycle_quality_score
    ORDER BY project_group, lifecycle_quality_score
"""))
print("\n=== LQS by project group ===")
print(lqs_detail.to_string())

# Lifecycle quality score bar chart
fig, ax = plt.subplots(figsize=(10, 6))
lqs_fast = lqs_detail[lqs_detail['project_group']=='Fast Projects'].copy()
lqs_other = lqs_detail[lqs_detail['project_group']=='Other Projects'].copy()

lqs_fast['pct'] = lqs_fast['cnt'] / lqs_fast['cnt'].sum() * 100
lqs_other['pct'] = lqs_other['cnt'] / lqs_other['cnt'].sum() * 100

x = np.arange(len(lqs_fast))
width = 0.35
ax.bar(x - width/2, lqs_fast['pct'], width, label='Fast Projects', color='coral', alpha=0.8)
ax.bar(x + width/2, lqs_other['pct'], width, label='Other Projects', color='steelblue', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels([f'LQS={v}' for v in lqs_fast['lifecycle_quality_score'].values])
ax.set_ylabel('Percentage of Issues (%)')
ax.set_title('Lifecycle Quality Score Distribution: Fast vs Other Projects')
ax.legend()
plt.tight_layout()
plt.savefig('/work/lifecycle_quality_distribution.png', dpi=150)
plt.close()

# Examine the engagement_risk_score and similar patterns
print("\n\n=== Risk Averages ===")
risk_detail = db.frame(db.query("""
    SELECT 
        project_name,
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity,
        AVG(intelligence_score) as avg_intel,
        AVG(collaboration_opportunity_score) as avg_collab,
        AVG(efficiency_opportunity_score) as avg_efficiency,
        AVG(process_opportunity_score) as avg_process_opp
    FROM jira__issue_intelligence_analytics
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY project_name
"""))
print(risk_detail.to_string())

# Overall averages for comparison
overall_risk = db.frame(db.query("""
    SELECT 
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity,
        AVG(collaboration_opportunity_score) as avg_collab,
        AVG(efficiency_opportunity_score) as avg_efficiency,
        AVG(process_opportunity_score) as avg_process_opp
    FROM jira__issue_intelligence_analytics
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
"""))
print("\n=== Overall Averages (Other Projects) ===")
print(overall_risk.to_string())

print("\n\nAll analysis complete.")