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

# Compute lifecycle_deviation_ratio
trajectory_risk_map = {
    'Excellent': 1, 'Improving': 2, 'Stable': 3, 
    'Volatile': 4, 'At Risk': 5, 'Deteriorating': 6, 'Declining': 7
}
projects['trajectory_risk_numeric'] = projects['trajectory_status'].map(trajectory_risk_map)

projects['lifecycle_deviation_ratio'] = (
    projects['trajectory_risk_numeric'] / 7 * 50 +
    (1 - (projects['resolution_velocity_change_percent'] - projects['resolution_velocity_change_percent'].min()) / 
         (projects['resolution_velocity_change_percent'].max() - projects['resolution_velocity_change_percent'].min())) * 25 +
    (projects['net_issue_growth_30d'] - projects['net_issue_growth_30d'].min()) / 
    (projects['net_issue_growth_30d'].max() - projects['net_issue_growth_30d'].min()) * 25
)

# Assignment risk score from team performance
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
stakeholders['cross_func_mismatch'] = abs(
    stakeholders['cross_functional_projects'] / stakeholders['cross_functional_projects'].max() * 100 -
    stakeholders['engagement_quality_score']
)

# Recompute fp and other AFTER adding columns
fp = projects[projects['is_false_prosperity']]
other = projects[~projects['is_false_prosperity']]

print("=== Lifecycle Deviation Ratio ===")
fp_life = fp['lifecycle_deviation_ratio'].mean()
ot_life = other['lifecycle_deviation_ratio'].mean()
print(f"False Prosperity: {fp_life:.2f}")
print(f"Other: {ot_life:.2f}")
stat, pval = stats.ttest_ind(fp['lifecycle_deviation_ratio'], other['lifecycle_deviation_ratio'])
print(f"t-test p-value: {pval:.4f}")

print("\n=== Assignment Risk Score ===")
hr_ids = stakeholders[stakeholders['engagement_risk_status']=='High Risk']['stakeholder_id']
mr_ids = stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['stakeholder_id']
hr_assign = team[team['user_id'].isin(hr_ids)]['assignment_risk_score'].mean()
mr_assign = team[team['user_id'].isin(mr_ids)]['assignment_risk_score'].mean()
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

# Figure 8: Hidden factors
fig, axes = plt.subplots(1, 3, figsize=(18, 6))

axes[0].boxplot([fp['lifecycle_deviation_ratio'], other['lifecycle_deviation_ratio']],
                tick_labels=['False Prosperity', 'Other'])
axes[0].set_ylabel('Lifecycle Deviation Ratio')
axes[0].set_title('Lifecycle Deviation Ratio by Project Group')

hr_assign_data = team[team['user_id'].isin(hr_ids)]['assignment_risk_score']
mr_assign_data = team[team['user_id'].isin(mr_ids)]['assignment_risk_score']
axes[1].boxplot([hr_assign_data, mr_assign_data], tick_labels=['High Risk', 'Medium Risk'])
axes[1].set_ylabel('Assignment Risk Score')
axes[1].set_title('Assignment Risk by Engagement Risk')

hr_mismatch_data = stakeholders[stakeholders['engagement_risk_status']=='High Risk']['cross_func_mismatch']
mr_mismatch_data = stakeholders[stakeholders['engagement_risk_status']=='Medium Risk']['cross_func_mismatch']
axes[2].boxplot([hr_mismatch_data, mr_mismatch_data], tick_labels=['High Risk', 'Medium Risk'])
axes[2].set_ylabel('Cross-Functional Mismatch Score')
axes[2].set_title('Cross-Functional Collaboration Mismatch')

plt.tight_layout()
plt.savefig('/work/fig8_hidden_factors.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 8 saved.")

# Detailed view of top false prosperity projects
print("\n\n=== DETAILED VIEW OF TOP 5 FALSE PROSPERITY PROJECTS ===")
top5 = fp.nlargest(5, 'overall_health_score')
for _, proj in top5.iterrows():
    print(f"\nProject: {proj['project_name']} ({proj['project_key']})")
    print(f"  Overall Health Score: {proj['overall_health_score']}")
    print(f"  True Health Score (reassessed): {proj['true_health_score']:.1f}" if 'true_health_score' in proj else f"  True Health Score: N/A")
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

# Summary
print("\n\n=== SUMMARY STATISTICS ===")
print(f"Total projects: {len(projects)}")
print(f"False prosperity projects: {len(fp)} ({len(fp)/len(projects)*100:.1f}%)")
print(f"Stakeholders with High Risk engagement: {len(stakeholders[stakeholders['engagement_risk_status']=='High Risk'])} ({len(stakeholders[stakeholders['engagement_risk_status']=='High Risk'])/len(stakeholders)*100:.1f}%)")
print(f"Team members with performance > 80: {len(team[team['overall_performance_score']>80])} ({len(team[team['overall_performance_score']>80])/len(team)*100:.1f}%)")

# Recompute the true health score model for the report
risk_cols = ['health_risk_score', 'schedule_risk_score', 'resource_risk_score', 
             'complexity_risk_score', 'scope_risk_score']
max_risk = projects[risk_cols].max().max()
min_risk = projects[risk_cols].min().min()
projects['risk_exposure'] = 100 * (1 - (projects[risk_cols].mean(axis=1) - min_risk) / (max_risk - min_risk))
projects['delivery_effectiveness'] = projects['value_delivery_percentage'] + 100 * projects['success_probability']
projects['delivery_effectiveness'] = projects['delivery_effectiveness'] / projects['delivery_effectiveness'].max() * 100
projects['lifecycle_health'] = (
    ((projects['resolution_velocity_change_percent'] - projects['resolution_velocity_change_percent'].min()) / 
     (projects['resolution_velocity_change_percent'].max() - projects['resolution_velocity_change_percent'].min())) * 50 +
    (1 - (projects['net_issue_growth_30d'] - projects['net_issue_growth_30d'].min()) / 
     (projects['net_issue_growth_30d'].max() - projects['net_issue_growth_30d'].min())) * 50
)
projects['operational_health'] = (
    projects['team_stability_percentage'] * 0.5 +
    projects['sprint_adoption_rate'] * 100 * 0.5
)
projects['true_health_score'] = (
    projects['risk_exposure'] * 0.35 +
    projects['delivery_effectiveness'] * 0.25 +
    projects['lifecycle_health'] * 0.20 +
    projects['operational_health'] * 0.20
)
projects['health_gap'] = projects['overall_health_score'] - projects['true_health_score']

fp2 = projects[projects['is_false_prosperity']]
print(f"\nFalse prosperity: mean reported health={fp2['overall_health_score'].mean():.1f}, mean true health={fp2['true_health_score'].mean():.1f}, mean gap={fp2['health_gap'].mean():.1f}")
print(f"Other: mean reported health={projects.loc[~projects['is_false_prosperity'],'overall_health_score'].mean():.1f}, mean true health={projects.loc[~projects['is_false_prosperity'],'true_health_score'].mean():.1f}, mean gap={projects.loc[~projects['is_false_prosperity'],'health_gap'].mean():.1f}")

# Correlation between lifecycle deviation and health gap
corr = projects[['lifecycle_deviation_ratio', 'health_gap', 'overall_health_score', 'total_risk_score']].corr()
print("\nCorrelations involving lifecycle_deviation_ratio:")
print(corr['lifecycle_deviation_ratio'])

projects.to_csv('/work/projects_final.csv', index=False)
print("\nDone. Files saved.")