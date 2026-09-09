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

projects['is_false_prosperity'] = (
    (projects['overall_health_score'] > 75) & 
    (projects['risk_category'].isin(['Critical Risk', 'High Risk'])) & 
    (projects['complexity_risk_score'] > 30)
)
fp = projects[projects['is_false_prosperity']]
other = projects[~projects['is_false_prosperity']]

# Figure 3: Team performance by engagement risk
team_stakeholder = team.merge(stakeholders, left_on='user_id', right_on='stakeholder_id', 
                              suffixes=('_team', '_stakeholder'))

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

metrics = [
    ('overall_performance_score', 'Performance Score'),
    ('resolution_rate_percentage', 'Resolution Rate'),
    ('avg_resolution_days', 'Avg Resolution Days'),
    ('consistency_percentage', 'Consistency'),
    ('avg_sprint_completion_rate', 'Sprint Completion Rate'),
    ('estimate_accuracy_percentage', 'Estimate Accuracy')
]
for i, (col, title) in enumerate(metrics):
    ax = axes[i//3, i%3]
    high_risk_data = team_stakeholder[team_stakeholder['engagement_risk_status'] == 'High Risk'][col].dropna()
    med_risk_data = team_stakeholder[team_stakeholder['engagement_risk_status'] == 'Medium Risk'][col].dropna()
    bp = ax.boxplot([high_risk_data, med_risk_data], tick_labels=['High Risk', 'Medium Risk'])
    ax.set_title(f'{title} by Engagement Risk')
    ax.set_ylabel(title)

plt.tight_layout()
plt.savefig('/work/fig3_team_perf_by_engagement.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

# Figure 4: Stakeholder engagement patterns
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

risk_colors = {'High Risk': '#e74c3c', 'Medium Risk': '#3498db'}
for status, color in risk_colors.items():
    subset = stakeholders[stakeholders['engagement_risk_status'] == status]
    axes[0,0].scatter(subset['engagement_breadth_score'], subset['engagement_depth_score'],
                      c=color, label=status, alpha=0.3, s=10)
axes[0,0].set_xlabel('Engagement Breadth Score')
axes[0,0].set_ylabel('Engagement Depth Score')
axes[0,0].set_title('Engagement Breadth vs Depth')
axes[0,0].legend()

for status, color in risk_colors.items():
    subset = stakeholders[stakeholders['engagement_risk_status'] == status]
    axes[0,1].scatter(subset['cross_functional_projects'], subset['engagement_quality_score'],
                      c=color, label=status, alpha=0.3, s=10)
axes[0,1].set_xlabel('Cross-Functional Projects')
axes[0,1].set_ylabel('Engagement Quality Score')
axes[0,1].set_title('Cross-Functional Projects vs Engagement Quality')
axes[0,1].legend()

archetype_counts = stakeholders.groupby(['engagement_risk_status', 'stakeholder_archetype']).size().unstack()
archetype_pct = archetype_counts.div(archetype_counts.sum(axis=1), axis=0)
archetype_pct.T.plot(kind='bar', ax=axes[1,0], color=['#e74c3c', '#3498db'])
axes[1,0].set_title('Stakeholder Archetype by Risk Status')
axes[1,0].set_ylabel('Proportion')
axes[1,0].legend(title='Engagement Risk')
axes[1,0].tick_params(axis='x', rotation=45)

influence_counts = stakeholders.groupby(['engagement_risk_status', 'influence_level']).size().unstack()
influence_pct = influence_counts.div(influence_counts.sum(axis=1), axis=0)
influence_pct.T.plot(kind='bar', ax=axes[1,1], color=['#e74c3c', '#3498db'])
axes[1,1].set_title('Influence Level by Risk Status')
axes[1,1].set_ylabel('Proportion')
axes[1,1].legend(title='Engagement Risk')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/fig4_stakeholder_patterns.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

# Part 2: Build comprehensive risk assessment model
print("\n=== PART 2: COMPREHENSIVE RISK MODEL ===")

# Build a True Health Score (THS) from multiple dimensions
# Dimension 1: Risk exposure (inverse of risk scores)
risk_cols = ['health_risk_score', 'schedule_risk_score', 'resource_risk_score', 
             'complexity_risk_score', 'scope_risk_score']
# Normalize risk scores to 0-100 range (lower is better, invert)
max_risk = projects[risk_cols].max().max()
min_risk = projects[risk_cols].min().min()

# Dimension 2: Delivery effectiveness
# value_delivery_percentage, success_probability

# Dimension 3: Issue lifecycle health
# resolution_velocity_change_percent (positive good), net_issue_growth_30d (negative good)

# Dimension 4: Team/operational health
# team_stability_percentage, sprint_adoption_rate

# Create standardized component scores (0-100, higher = healthier)
projects['risk_exposure'] = 100 * (1 - (projects[risk_cols].mean(axis=1) - min_risk) / (max_risk - min_risk))
projects['delivery_effectiveness'] = projects['value_delivery_percentage'] + 100 * projects['success_probability']
projects['delivery_effectiveness'] = projects['delivery_effectiveness'] / projects['delivery_effectiveness'].max() * 100

projects['lifecycle_health'] = (
    (projects['resolution_velocity_change_percent'] - projects['resolution_velocity_change_percent'].min()) / 
    (projects['resolution_velocity_change_percent'].max() - projects['resolution_velocity_change_percent'].min()) * 50 +
    (1 - (projects['net_issue_growth_30d'] - projects['net_issue_growth_30d'].min()) / 
     (projects['net_issue_growth_30d'].max() - projects['net_issue_growth_30d'].min())) * 50
)

projects['operational_health'] = (
    projects['team_stability_percentage'] * 0.5 +
    projects['sprint_adoption_rate'] * 100 * 0.5
)

# Composite True Health Score (equal weights)
projects['true_health_score'] = (
    projects['risk_exposure'] * 0.35 +
    projects['delivery_effectiveness'] * 0.25 +
    projects['lifecycle_health'] * 0.20 +
    projects['operational_health'] * 0.20
)

# Gap = original health - true health (positive gap = overrated)
projects['health_gap'] = projects['overall_health_score'] - projects['true_health_score']

print("\nTrue Health Score for false prosperity vs others:")
print(fp.assign(t = projects.loc[fp.index, 'true_health_score'])[['overall_health_score','t','health_gap']].describe())
print("\nOther:")
print(other.assign(t = projects.loc[other.index, 'true_health_score'])[['overall_health_score','t','health_gap']].describe())

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

# Figure 5: Original vs True Health Score
fig, ax = plt.subplots(figsize=(10, 8))
colors = ['#e74c3c' if x else '#2ecc71' for x in projects['is_false_prosperity']]
ax.scatter(projects['overall_health_score'], projects['true_health_score'], 
           c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
ax.plot([40, 100], [40, 100], 'k--', alpha=0.5, label='y=x (no change)')
ax.set_xlabel('Reported Overall Health Score')
ax.set_ylabel('Reassessed True Health Score')
ax.set_title('Reported Health vs Reassessed True Health')
ax.legend(loc='lower right')
# Annotate top overrated
top_overrated = projects.nlargest(8, 'health_gap')
for _, row in top_overrated.iterrows():
    ax.annotate(row['project_name'][:15], (row['overall_health_score'], row['true_health_score']),
                fontsize=8, alpha=0.7)
plt.tight_layout()
plt.savefig('/work/fig5_true_health_model.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 5 saved.")

# Figure 6: Health gap histogram
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].hist(projects[projects['is_false_prosperity']]['health_gap'], bins=15, alpha=0.7, color='#e74c3c', label='False Prosperity')
axes[0].hist(projects[~projects['is_false_prosperity']]['health_gap'], bins=20, alpha=0.7, color='#2ecc71', label='Other')
axes[0].axvline(x=0, color='black', linestyle='--')
axes[0].set_xlabel('Health Gap (Reported - True)')
axes[0].set_ylabel('Count')
axes[0].set_title('Distribution of Health Gap')
axes[0].legend()

# Boxplot of gap by group
axes[1].boxplot([projects[projects['is_false_prosperity']]['health_gap'], 
                 projects[~projects['is_false_prosperity']]['health_gap']],
                tick_labels=['False Prosperity', 'Other'])
axes[1].set_ylabel('Health Gap')
axes[1].set_title('Health Gap by Group')
axes[1].axhline(y=0, color='black', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig('/work/fig6_health_gap.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 6 saved.")

# Save computed model for later use
projects.to_csv('/work/projects_with_model.csv', index=False)
print("\nSaved projects_with_model.csv")