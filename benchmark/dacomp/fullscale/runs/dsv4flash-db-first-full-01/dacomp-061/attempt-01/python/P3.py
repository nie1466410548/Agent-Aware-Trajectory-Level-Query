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
        CASE WHEN regression_ratio = 0.0 THEN 'No Regression'
             WHEN regression_ratio = 0.1 THEN 'Some Regression'
             ELSE 'High Regression'
        END as regression_level,
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
    print(f"  {row['regression_level']}: {row['cnt']} ({row['cnt']/total_fast*100:.1f}%)")

reg_slow = db.frame(db.query("""
    SELECT 
        CASE WHEN regression_ratio = 0.0 THEN 'No Regression'
             WHEN regression_ratio = 0.1 THEN 'Some Regression'
             ELSE 'High Regression'
        END as regression_level,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio
"""))
print("\n=== Regression ratio distribution for OTHER projects ===")
total_slow = reg_slow['cnt'].sum()
for _, row in reg_slow.iterrows():
    print(f"  {row['regression_level']}: {row['cnt']} ({row['cnt']/total_slow*100:.1f}%)")

# Chi-squared test for independence
from scipy.stats import chi2_contingency
cont_table = np.array([
    [reg_fast[reg_fast['regression_level']=='No Regression']['cnt'].iloc[0],
     reg_fast[reg_fast['regression_level']=='Some Regression']['cnt'].iloc[0],
     reg_fast[reg_fast['regression_level']=='High Regression']['cnt'].iloc[0]],
    [reg_slow[reg_slow['regression_level']=='No Regression']['cnt'].iloc[0],
     reg_slow[reg_slow['regression_level']=='Some Regression']['cnt'].iloc[0],
     reg_slow[reg_slow['regression_level']=='High Regression']['cnt'].iloc[0]]
])
chi2, p_val, dof, expected = chi2_contingency(cont_table)
print(f"\nChi-squared test: chi2={chi2:.2f}, p={p_val:.4f}")

# Create a pie chart comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
labels = ['No Regression (0.0)', 'Some Regression (0.1)', 'High Regression (0.2)']
colors_pie = ['#4CAF50', '#FFC107', '#F44336']

# Fast projects
fast_vals = [reg_fast[reg_fast['regression_level']=='No Regression']['cnt'].iloc[0],
             reg_fast[reg_fast['regression_level']=='Some Regression']['cnt'].iloc[0],
             reg_fast[reg_fast['regression_level']=='High Regression']['cnt'].iloc[0]]
axes[0].pie(fast_vals, labels=labels, autopct='%1.1f%%', colors=colors_pie, startangle=90)
axes[0].set_title('Fast Projects (avg_close < 15d)\nRegression Ratio Distribution')

# Other projects
slow_vals = [reg_slow[reg_slow['regression_level']=='No Regression']['cnt'].iloc[0],
             reg_slow[reg_slow['regression_level']=='Some Regression']['cnt'].iloc[0],
             reg_slow[reg_slow['regression_level']=='High Regression']['cnt'].iloc[0]]
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
lqs_fast = db.frame(db.query("""
    SELECT lifecycle_quality_score, COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY lifecycle_quality_score
    ORDER BY lifecycle_quality_score
"""))
print(f"Fast projects LQS values: {lqs_fast['lifecycle_quality_score'].tolist()}")
print(f"Fast projects LQS counts: {lqs_fast['cnt'].tolist()}")

lqs_slow = db.frame(db.query("""
    SELECT lifecycle_quality_score, COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY lifecycle_quality_score
    ORDER BY lifecycle_quality_score
"""))
print(f"Other projects LQS values: {lqs_slow['lifecycle_quality_score'].tolist()}")
print(f"Other projects LQS counts: {lqs_slow['cnt'].tolist()}")

# Check the composition of lifecyle quality scores
print("\n\n=== Lifecycle Quality Score Distribution Summary ===")
lqs_fast_total = lqs_fast['cnt'].sum()
lqs_slow_total = lqs_slow['cnt'].sum()
for _, row in lqs_fast.iterrows():
    pct = row['cnt'] / lqs_fast_total * 100
    print(f"  Fast: LQS={row['lifecycle_quality_score']:.0f}: {row['cnt']} ({pct:.1f}%)")
for _, row in lqs_slow.iterrows():
    pct = row['cnt'] / lqs_slow_total * 100
    print(f"  Other: LQS={row['lifecycle_quality_score']:.0f}: {row['cnt']} ({pct:.1f}%)")

# Examine the assignment_risk_score and engagement_risk_score patterns
# which are 0 for all rows in fast projects (based on issue_agg data)
print("\n\n=== Risk Score Details ===")
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

# Check the distribution of lifecycle_quality_score for all projects
print("\n\n=== Lifecycle_quality_score complete distribution ===")
lqs_all = db.frame(db.query("""
    SELECT lifecycle_quality_score, COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY lifecycle_quality_score
    ORDER BY lifecycle_quality_score
"""))
print(lqs_all.to_string())

print("\n\nAnalysis complete.")