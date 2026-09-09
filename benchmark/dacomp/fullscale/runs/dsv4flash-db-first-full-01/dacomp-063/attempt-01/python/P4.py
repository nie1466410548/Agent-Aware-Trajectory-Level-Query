import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Reload data
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

# ===== PART 2: COMPREHENSIVE RISK ASSESSMENT MODEL =====
# Build a multi-dimensional True Health Score

# Dimension 1: Risk exposure (inverse of 5 risk sub-scores)
risk_cols = ['health_risk_score', 'schedule_risk_score', 'resource_risk_score', 
             'complexity_risk_score', 'scope_risk_score']
max_risk = projects[risk_cols].max().max()
min_risk = projects[risk_cols].min().min()

# Risk exposure: 100 = lowest risk (best), 0 = highest risk (worst)
projects['risk_exposure'] = 100 * (1 - (projects[risk_cols].mean(axis=1) - min_risk) / (max_risk - min_risk))

# Dimension 2: Delivery effectiveness
projects['delivery_effectiveness'] = projects['value_delivery_percentage'] + 100 * projects['success_probability']
projects['delivery_effectiveness'] = projects['delivery_effectiveness'] / projects['delivery_effectiveness'].max() * 100

# Dimension 3: Issue lifecycle health (velocity change + issue growth)
vel_min = projects['resolution_velocity_change_percent'].min()
vel_max = projects['resolution_velocity_change_percent'].max()
issue_min = projects['net_issue_growth_30d'].min()
issue_max = projects['net_issue_growth_30d'].max()

projects['lifecycle_health'] = (
    ((projects['resolution_velocity_change_percent'] - vel_min) / (vel_max - vel_min)) * 50 +
    (1 - (projects['net_issue_growth_30d'] - issue_min) / (issue_max - issue_min)) * 50
)

# Dimension 4: Operational health (team stability + sprint adoption)
projects['operational_health'] = (
    projects['team_stability_percentage'] * 0.5 +
    projects['sprint_adoption_rate'] * 100 * 0.5
)

# Composite True Health Score (weighted)
projects['true_health_score'] = (
    projects['risk_exposure'] * 0.35 +
    projects['delivery_effectiveness'] * 0.25 +
    projects['lifecycle_health'] * 0.20 +
    projects['operational_health'] * 0.20
)

# Gap = reported health - true health (positive = overrated)
projects['health_gap'] = projects['overall_health_score'] - projects['true_health_score']

# Now fp and other should have access
fp = projects[projects['is_false_prosperity']]
other = projects[~projects['is_false_prosperity']]

print("True Health Score for false prosperity:")
print(fp[['overall_health_score', 'true_health_score', 'health_gap']].describe())
print("\nTrue Health Score for other projects:")
print(other[['overall_health_score', 'true_health_score', 'health_gap']].describe())

# Correlation of health_gap with key variables
gap_corrs = projects[['health_gap', 'overall_health_score', 'total_risk_score', 'complexity_risk_score',
                      'success_probability', 'value_delivery_percentage', 'net_issue_growth_30d',
                      'resolution_velocity_change_percent', 'team_stability_percentage',
                      'high_delay_cost_issues', 'total_hours_invested']].corr()['health_gap'].sort_values()
print("\nCorrelation of health_gap with key variables:")
print(gap_corrs)

# Top overrated projects
print("\nTop 15 most overrated projects (largest health_gap):")
overrated = projects.nlargest(15, 'health_gap')[['project_id', 'project_name', 'overall_health_score', 
                                                  'true_health_score', 'health_gap', 'total_risk_score',
                                                  'risk_category', 'complexity_risk_score']]
print(overrated.to_string(index=False))

# ===== PART 3: ROOT CAUSE ANALYSIS =====
print("\n\n=== PART 3: ROOT CAUSE ANALYSIS ===")

# Staffing efficiency factors from team performance
print("\nStaffing efficiency for High Risk engagement stakeholders:")
team_stakeholder = team.merge(stakeholders, left_on='user_id', right_on='stakeholder_id', 
                              suffixes=('_team', '_stakeholder'))

hr_team = team_stakeholder[team_stakeholder['engagement_risk_status'] == 'High Risk']
mr_team = team_stakeholder[team_stakeholder['engagement_risk_status'] == 'Medium Risk']

for col in ['overall_performance_score', 'resolution_rate_percentage', 'avg_resolution_days',
            'estimate_accuracy_percentage', 'consistency_percentage', 'unique_collaborators_on_issues',
            'at_churn_risk', 'inactive_recently', 'poor_estimation', 'linked_issues']:
    hr_mean = hr_team[col].mean()
    mr_mean = mr_team[col].mean()
    stat, pval = stats.ttest_ind(hr_team[col].dropna(), mr_team[col].dropna(), equal_var=False)
    print(f"  {col}: HighRisk={hr_mean:.3f}, MedRisk={mr_mean:.3f}, p={pval:.4f}")

# Communication network quality
print("\nCommunication & Collaboration Network:")
for col in ['direct_network_connections', 'total_outbound_influence', 'total_inbound_influence',
            'cross_functional_projects', 'engagement_breadth_score', 'engagement_depth_score',
            'engagement_quality_score', 'engagement_impact_score', 'total_engagement_score',
            'issues_reported', 'issues_assigned', 'total_comments_authored']:
    hr_mean = stakeholders[stakeholders['engagement_risk_status']=='High Risk'][col].mean()
    mr_mean = stakeholders[stakeholders['engagement_risk_status']=='Medium Risk'][col].mean()
    stat, pval = stats.ttest_ind(
        stakeholders[stakeholders['engagement_risk_status']=='High Risk'][col].dropna(),
        stakeholders[stakeholders['engagement_risk_status']=='Medium Risk'][col].dropna(),
        equal_var=False)
    print(f"  {col}: HighRisk={hr_mean:.3f}, MedRisk={mr_mean:.3f}, p={pval:.4f}")

# Workflow deviations from project table
print("\nWorkflow Deviation Indicators (False Prosperity vs Other):")
for col in ['resolution_velocity_change_percent', 'net_issue_growth_30d', 'high_delay_cost_issues',
            'value_delivery_percentage', 'team_stability_percentage', 'total_hours_invested',
            'estimated_project_value_points', 'delivered_value_points', 'sprint_adoption_rate',
            'total_risk_score', 'success_probability']:
    fp_mean = fp[col].mean()
    ot_mean = other[col].mean()
    stat, pval = stats.ttest_ind(fp[col].dropna(), other[col].dropna(), equal_var=False)
    print(f"  {col}: FP={fp_mean:.3f}, Others={ot_mean:.3f}, p={pval:.4f}")

# Figure 5: Original vs True Health Score
fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#e74c3c' if x else '#2ecc71' for x in projects['is_false_prosperity']]
ax.scatter(projects['overall_health_score'], projects['true_health_score'], 
           c=colors, alpha=0.6, edgecolors='black', linewidth=0.5, s=60)
ax.plot([40, 100], [40, 100], 'k--', alpha=0.5, label='y=x (no change)')
ax.set_xlabel('Reported Overall Health Score')
ax.set_ylabel('Reassessed True Health Score')
ax.set_title('Reported Health vs Reassessed True Health')
ax.legend(loc='lower right')
# Annotate top overrated
top_overrated = projects.nlargest(8, 'health_gap')
for _, row in top_overrated.iterrows():
    ax.annotate(row['project_name'][:12], (row['overall_health_score'], row['true_health_score']),
                fontsize=8, alpha=0.7)
plt.tight_layout()
plt.savefig('/work/fig5_true_health_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved.")

# Figure 6: Health gap histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].hist(fp['health_gap'], bins=10, alpha=0.7, color='#e74c3c', label='False Prosperity')
axes[0].hist(other['health_gap'], bins=20, alpha=0.7, color='#2ecc71', label='Other')
axes[0].axvline(x=0, color='black', linestyle='--')
axes[0].set_xlabel('Health Gap (Reported - True)')
axes[0].set_ylabel('Count')
axes[0].set_title('Distribution of Health Gap')
axes[0].legend()

axes[1].boxplot([fp['health_gap'], other['health_gap']],
                tick_labels=['False Prosperity', 'Other'])
axes[1].set_ylabel('Health Gap')
axes[1].set_title('Health Gap by Group')
axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/work/fig6_health_gap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

# Figure 7: Component breakdown for false prosperity projects
fig, ax = plt.subplots(figsize=(12, 8))
components = ['risk_exposure', 'delivery_effectiveness', 'lifecycle_health', 'operational_health']
fp_means = [fp[c].mean() for c in components]
ot_means = [other[c].mean() for c in components]

x = np.arange(len(components))
width = 0.35
ax.bar(x - width/2, fp_means, width, label='False Prosperity', color='#e74c3c', alpha=0.8)
ax.bar(x + width/2, ot_means, width, label='Other Projects', color='#2ecc71', alpha=0.8)
ax.set_xticks(x)
ax.set_xticklabels(['Risk Exposure\n(inverted)', 'Delivery\nEffectiveness', 'Lifecycle\nHealth', 'Operational\nHealth'])
ax.set_ylabel('Score (0-100)')
ax.set_title('Component Breakdown: False Prosperity vs Other Projects')
ax.legend()
ax.set_ylim(0, 100)
plt.tight_layout()
plt.savefig('/work/fig7_component_breakdown.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 7 saved.")

# Save all results
projects.to_csv('/work/projects_with_model.csv', index=False)
print("\nAll figures and data saved successfully.")