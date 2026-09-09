import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Reload
projects = db.frame(db.query("SELECT * FROM jira__project_risk_assessment"))
stakeholders = db.frame(db.query("SELECT * FROM jira__stakeholder_engagement_insights"))
team = db.frame(db.query("SELECT * FROM jira__team_performance_dashboard"))

# Define false prosperity
projects['is_false_prosperity'] = (
    (projects['overall_health_score'] > 75) & 
    (projects['risk_category'].isin(['Critical Risk', 'High Risk'])) & 
    (projects['complexity_risk_score'] > 30)
)
fp = projects[projects['is_false_prosperity']]
other = projects[~projects['is_false_prosperity']]

# Compute lifecycle_deviation_ratio
# This measures how much the project's trajectory deviates from what would be expected
# given its health score. It's the ratio of actual trajectory risk to expected trajectory.
# resolution_velocity_change_percent: negative = declining velocity
# net_issue_growth_30d: positive = growing issue backlog
# trajectory_status: maps to numeric risk

trajectory_risk_map = {
    'Excellent': 1, 'Improving': 2, 'Stable': 3, 
    'Volatile': 4, 'At Risk': 5, 'Deteriorating': 6, 'Declining': 7
}
projects['trajectory_risk_numeric'] = projects['trajectory_status'].map(trajectory_risk_map)

# Lifecycle deviation: combines trajectory risk, velocity change, issue growth
# Higher = more deviation from healthy lifecycle
projects['lifecycle_deviation_ratio'] = (
    projects['trajectory_risk_numeric'] / 7 * 50 +  # 0-50
    (1 - (projects['resolution_velocity_change_percent'] - projects['resolution_velocity_change_percent'].min()) / 
         (projects['resolution_velocity_change_percent'].max() - projects['resolution_velocity_change_percent'].min())) * 25 +  # 0-25
    (projects['net_issue_growth_30d'] - projects['net_issue_growth_30d'].min()) / 
    (projects['net_issue_growth_30d'].max() - projects['net_issue_growth_30d'].min()) * 25  # 0-25
)

# Assignment risk score: from team performance data
# Combines: at_churn_risk, inactive_recently, poor_estimation, 
# low consistency, low resolution rate, high resolution days
team['assignment_risk_score'] = (
    team['at_churn_risk'] * 25 +
    team['inactive_recently'] * 20 +
    team['poor_estimation'] * 15 +
    (1 - team['consistency_percentage']) * 20 +
    (1 - team['resolution_rate_percentage']) * 10 +
    (team['avg_resolution_days'] / team['avg_resolution_days'].max()) * 10
)
team['assignment_risk_score'] = team['assignment_risk_score'] / team['assignment_risk_score'].max() * 100

# Cross-functional projects mismatch
# Compare cross_functional_projects (involvement breadth) with actual engagement quality
stakeholders['cross_func_mismatch'] = abs(
    stakeholders['cross_functional_projects'] / stakeholders['cross_functional_projects'].max() * 100 -
    stakeholders['engagement_quality_score']
)

print("=== Lifecycle Deviation Ratio ===")
fp_life = fp['lifecycle_deviation_ratio'].mean()
ot_life = other['lifecycle_deviation_ratio'].mean()
print(f"False Prosperity: {fp_life:.2f}")
print(f"Other: {ot_life:.2f}")
stat, pval = stats.ttest_ind(fp['lifecycle_deviation_ratio'], other['lifecycle_deviation_ratio'])
print(f"t-test p-value: {pval:.4f}")

print("\n=== Assignment Risk Score ===")
hr_assign = team[team['user_id'].isin(stakeholders[stakeholders['engagement_risk_status']=='High Risk']['stakeholder_id'])]['assignment_risk_score'].mean()
mr_assign = team[team['user_id'].isin(stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['stakeholder_id'])]['assignment_risk_score'].mean()
print(f"High Risk stakeholders: {hr_assign:.2f}")
print(f"Medium Risk stakeholders: {mr_assign:.2f}")

print("\n=== Cross-Functional Projects Mismatch ===")
hr_mismatch = stakeholders[stakeholders['engagement_risk_status']=='High Risk']['cross_func_mismatch'].mean()
mr_mismatch = stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['cross_func_mismatch'].mean()
print(f"High Risk: {hr_mismatch:.2f}")
print(f"Medium Risk: {mr_mismatch:.2f}")
stat, pval = stats.ttest_ind(
    stakeholders[stakeholders['engagement_risk_status']=='High Risk']['cross_func_mismatch'],
    stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['cross_func_mismatch']
)
print(f"t-test p-value: {pval:.4f}")

# Figure 8: Lifecycle deviation by group
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# Lifecycle deviation
axes[0].boxplot([fp['lifecycle_deviation_ratio'], other['lifecycle_deviation_ratio']],
                tick_labels=['False Prosperity', 'Other'])
axes[0].set_ylabel('Lifecycle Deviation Ratio')
axes[0].set_title('Lifecycle Deviation Ratio by Project Group')

# Assignment risk by engagement risk
hr_assign_data = team[team['user_id'].isin(stakeholders[stakeholders['engagement_risk_status']=='High Risk']['stakeholder_id'])]['assignment_risk_score']
mr_assign_data = team[team['user_id'].isin(stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['stakeholder_id'])]['assignment_risk_score']
axes[1].boxplot([hr_assign_data, mr_assign_data], tick_labels=['High Risk', 'Medium Risk'])
axes[1].set_ylabel('Assignment Risk Score')
axes[1].set_title('Assignment Risk by Stakeholder Engagement Risk')

# Cross-functional mismatch
hr_mismatch_data = stakeholders[stakeholders['engagement_risk_status']=='High Risk']['cross_func_mismatch']
mr_mismatch_data = stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['cross_func_mismatch']
axes[2].boxplot([hr_mismatch_data, mr_mismatch_data], tick_labels=['High Risk', 'Medium Risk'])
axes[2].set_ylabel('Cross-Functional Mismatch Score')
axes[2].set_title('Cross-Functional Collaboration Mismatch')

plt.tight_layout()
plt.savefig('/work/fig8_hidden_factors.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 8 saved.")

# Detailed summary of top false prosperity projects
print("\n\n=== DETAILED VIEW OF TOP 5 FALSE PROSPERITY PROJECTS ===")
top5 = fp.nlargest(5, 'overall_health_score')
for _, proj in top5.iterrows():
    print(f"\nProject: {proj['project_name']} ({proj['project_key']})")
    print(f"  Overall Health Score: {proj['overall_health_score']}")
    print(f"  True Health Score (reassessed): {proj['true_health_score']:.1f}")
    print(f"  Health Gap: {proj['health_gap']:.1f}")
    print(f"  Risk Category: {proj['risk_category']}")
    print(f"  Total Risk Score: {proj['total_risk_score']}")
    print(f"  Complexity Risk: {proj['complexity_risk_score']}")
    print(f"  Trajectory: {proj['trajectory_status']}")
    print(f"  Value Delivery: {proj['value_delivery_percentage']:.1f}%")
    print(f"  Success Probability: {proj['success_probability']:.2f}")
    print(f"  Resolution Velocity Change: {proj['resolution_velocity_change_percent']:.1f}%")
    print(f"  Net Issue Growth (30d): {proj['net_issue_growth_30d']}")
    print(f"  Lifecycle Deviation Ratio: {proj['lifecycle_deviation_ratio']:.1f}")
    print(f"  Primary Risk Driver: {proj['primary_risk_driver']}")
    print(f"  Recommended Intervention: {proj['recommended_intervention']}")

# Save final summary
print("\n\n=== SUMMARY STATISTICS ===")
print(f"Total projects: {len(projects)}")
print(f"False prosperity projects: {len(fp)} ({len(fp)/len(projects)*100:.1f}%)")
print(f"Average health gap (FP): {fp['health_gap'].mean():.1f}")
print(f"Average health gap (Other): {other['health_gap'].mean():.1f}")
print(f"Stakeholders with High Risk engagement: {len(stakeholders[stakeholders['engagement_risk_status']=='High Risk'])} ({len(stakeholders[stakeholders['engagement_risk_status']=='High Risk'])/len(stakeholders)*100:.1f}%)")
print(f"Team members with performance > 80: {len(team[team['overall_performance_score']>80])} ({len(team[team['overall_performance_score']>80])/len(team)*100:.1f}%)")
print(f"High performers who are High Risk stakeholders: {len(team_stakeholder[(team_stakeholder['overall_performance_score']>80) & (team_stakeholder['engagement_risk_status']=='High Risk')])}")