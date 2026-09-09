import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load all data from the database
# Projects
projects_rows = db.rows(db.query("SELECT * FROM jira__project_risk_assessment"))
projects = pd.DataFrame(projects_rows)

# Stakeholders
stakeholder_rows = db.rows(db.query("SELECT * FROM jira__stakeholder_engagement_insights"))
stakeholders = pd.DataFrame(stakeholder_rows)

# Team performance
team_rows = db.rows(db.query("SELECT * FROM jira__team_performance_dashboard"))
team = pd.DataFrame(team_rows)

print("Data shapes:")
print(f"Projects: {projects.shape}")
print(f"Stakeholders: {stakeholders.shape}")
print(f"Team: {team.shape}")

# Define the false prosperity group
projects['is_false_prosperity'] = (
    (projects['overall_health_score'] > 75) & 
    (projects['risk_category'].isin(['Critical Risk', 'High Risk'])) & 
    (projects['complexity_risk_score'] > 30)
)

print(f"\nFalse prosperity projects: {projects['is_false_prosperity'].sum()}")
print(f"Other projects: {(~projects['is_false_prosperity']).sum()}")

# Part 1: Distribution characteristics
print("\n=== PART 1: Distribution Characteristics ===")
fp = projects[projects['is_false_prosperity']]
other = projects[~projects['is_false_prosperity']]

# Health score distribution
print("\nHealth score distribution for false prosperity projects:")
print(fp['overall_health_score'].describe())
print("\nHealth score distribution for other projects:")
print(other['overall_health_score'].describe())

# Risk category distribution
print("\nRisk category distribution for false prosperity:")
print(fp['risk_category'].value_counts())
print("\nRisk category distribution for others:")
print(other['risk_category'].value_counts())

# Trajectory status
print("\nTrajectory status for false prosperity:")
print(fp['trajectory_status'].value_counts())
print("\nTrajectory status for others:")
print(other['trajectory_status'].value_counts())

# Correlation analysis
print("\n\nCorrelation between health score and risk scores:")
corr_cols = ['overall_health_score', 'total_risk_score', 'health_risk_score', 
             'schedule_risk_score', 'resource_risk_score', 'complexity_risk_score',
             'scope_risk_score', 'success_probability', 'value_delivery_percentage',
             'team_stability_percentage', 'resolution_velocity_change_percent',
             'net_issue_growth_30d', 'high_delay_cost_issues']
corr_matrix = projects[corr_cols].corr()
print(corr_matrix['overall_health_score'].sort_values(ascending=False))

# Create figure 1: Health Score vs Risk Score scatter
fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# 1. Health vs Total Risk
colors = ['#e74c3c' if x else '#2ecc71' for x in projects['is_false_prosperity']]
axes[0,0].scatter(projects['overall_health_score'], projects['total_risk_score'], 
                  c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[0,0].set_xlabel('Overall Health Score')
axes[0,0].set_ylabel('Total Risk Score')
axes[0,0].set_title('Health Score vs Total Risk Score')
axes[0,0].axvline(x=75, color='gray', linestyle='--', alpha=0.5)
axes[0,0].axhline(y=projects['total_risk_score'].median(), color='gray', linestyle='--', alpha=0.5)

# 2. Health vs Complexity Risk
axes[0,1].scatter(projects['overall_health_score'], projects['complexity_risk_score'],
                  c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[0,1].set_xlabel('Overall Health Score')
axes[0,1].set_ylabel('Complexity Risk Score')
axes[0,1].set_title('Health Score vs Complexity Risk')
axes[0,1].axvline(x=75, color='gray', linestyle='--', alpha=0.5)
axes[0,1].axhline(y=30, color='gray', linestyle='--', alpha=0.5)

# 3. Health vs Success Probability
axes[0,2].scatter(projects['overall_health_score'], projects['success_probability'],
                  c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[0,2].set_xlabel('Overall Health Score')
axes[0,2].set_ylabel('Success Probability')
axes[0,2].set_title('Health Score vs Success Probability')
axes[0,2].axvline(x=75, color='gray', linestyle='--', alpha=0.5)

# 4. Health vs Value Delivery
axes[1,0].scatter(projects['overall_health_score'], projects['value_delivery_percentage'],
                  c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[1,0].set_xlabel('Overall Health Score')
axes[1,0].set_ylabel('Value Delivery %')
axes[1,0].set_title('Health Score vs Value Delivery')
axes[1,0].axvline(x=75, color='gray', linestyle='--', alpha=0.5)

# 5. Health vs Resolution Velocity Change
axes[1,1].scatter(projects['overall_health_score'], projects['resolution_velocity_change_percent'],
                  c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[1,1].set_xlabel('Overall Health Score')
axes[1,1].set_ylabel('Resolution Velocity Change %')
axes[1,1].set_title('Health Score vs Resolution Velocity')
axes[1,1].axvline(x=75, color='gray', linestyle='--', alpha=0.5)

# 6. Health vs Team Stability
axes[1,2].scatter(projects['overall_health_score'], projects['team_stability_percentage'],
                  c=colors, alpha=0.6, edgecolors='black', linewidth=0.5)
axes[1,2].set_xlabel('Overall Health Score')
axes[1,2].set_ylabel('Team Stability %')
axes[1,2].set_title('Health Score vs Team Stability')
axes[1,2].axvline(x=75, color='gray', linestyle='--', alpha=0.5)

plt.tight_layout()
plt.savefig('/work/fig1_health_vs_risk_scatter.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 1 saved.")

# Figure 2: Radar chart comparison
fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(polar=True))

categories = ['Health Risk', 'Schedule Risk', 'Resource Risk', 'Complexity Risk', 'Scope Risk']
fp_means = [fp['health_risk_score'].mean(), fp['schedule_risk_score'].mean(), 
            fp['resource_risk_score'].mean(), fp['complexity_risk_score'].mean(),
            fp['scope_risk_score'].mean()]
other_means = [other['health_risk_score'].mean(), other['schedule_risk_score'].mean(), 
               other['resource_risk_score'].mean(), other['complexity_risk_score'].mean(),
               other['scope_risk_score'].mean()]

N = len(categories)
angles = [n / float(N) * 2 * np.pi for n in range(N)]
angles += angles[:1]

fp_means += fp_means[:1]
other_means += other_means[:1]

ax.plot(angles, fp_means, 'o-', linewidth=2, label='False Prosperity', color='#e74c3c')
ax.fill(angles, fp_means, alpha=0.25, color='#e74c3c')
ax.plot(angles, other_means, 'o-', linewidth=2, label='Other Projects', color='#2ecc71')
ax.fill(angles, other_means, alpha=0.25, color='#2ecc71')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories, fontsize=12)
ax.set_ylim(0, 55)
ax.set_title('Risk Profile Comparison: False Prosperity vs Other Projects', fontsize=14, pad=20)
ax.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
plt.tight_layout()
plt.savefig('/work/fig2_radar_comparison.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 2 saved.")

# Figure 3: Team performance distribution by engagement risk
team_stakeholder = team.merge(stakeholders, left_on='user_id', right_on='stakeholder_id', 
                              suffixes=('_team', '_stakeholder'))

fig, axes = plt.subplots(2, 3, figsize=(18, 12))

# Performance score by engagement risk
for i, (col, title) in enumerate([
    ('overall_performance_score', 'Performance Score'),
    ('resolution_rate_percentage', 'Resolution Rate'),
    ('avg_resolution_days', 'Avg Resolution Days'),
    ('consistency_percentage', 'Consistency'),
    ('avg_sprint_completion_rate', 'Sprint Completion Rate'),
    ('estimate_accuracy_percentage', 'Estimate Accuracy')
]):
    ax = axes[i//3, i%3]
    data = [team_stakeholder[team_stakeholder['engagement_risk_status'] == 'High Risk'][col].dropna(),
            team_stakeholder[team_stakeholder['engagement_risk_status'] == 'Medium Risk'][col].dropna()]
    ax.boxplot(data, labels=['High Risk', 'Medium Risk'])
    ax.set_title(f'{title} by Engagement Risk')
    ax.set_ylabel(title)

plt.tight_layout()
plt.savefig('/work/fig3_team_perf_by_engagement.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 3 saved.")

# Figure 4: Stakeholder engagement patterns
fig, axes = plt.subplots(2, 2, figsize=(14, 12))

# Engagement breadth vs depth
risk_colors = {'High Risk': '#e74c3c', 'Medium Risk': '#3498db'}
for status, color in risk_colors.items():
    subset = stakeholders[stakeholders['engagement_risk_status'] == status]
    axes[0,0].scatter(subset['engagement_breadth_score'], subset['engagement_depth_score'],
                      c=color, label=status, alpha=0.3, s=10)
axes[0,0].set_xlabel('Engagement Breadth Score')
axes[0,0].set_ylabel('Engagement Depth Score')
axes[0,0].set_title('Engagement Breadth vs Depth')
axes[0,0].legend()

# Cross-functional projects vs engagement quality
for status, color in risk_colors.items():
    subset = stakeholders[stakeholders['engagement_risk_status'] == status]
    axes[0,1].scatter(subset['cross_functional_projects'], subset['engagement_quality_score'],
                      c=color, label=status, alpha=0.3, s=10)
axes[0,1].set_xlabel('Cross-Functional Projects')
axes[0,1].set_ylabel('Engagement Quality Score')
axes[0,1].set_title('Cross-Functional Projects vs Engagement Quality')
axes[0,1].legend()

# Stakeholder archetype distribution
archetype_counts = stakeholders.groupby(['engagement_risk_status', 'stakeholder_archetype']).size().unstack()
archetype_pct = archetype_counts.div(archetype_counts.sum(axis=1), axis=0)
archetype_pct.T.plot(kind='bar', ax=axes[1,0], color=['#e74c3c', '#3498db'])
axes[1,0].set_title('Stakeholder Archetype Distribution by Risk Status')
axes[1,0].set_ylabel('Proportion')
axes[1,0].legend(title='Engagement Risk')
axes[1,0].tick_params(axis='x', rotation=45)

# Influence level
influence_counts = stakeholders.groupby(['engagement_risk_status', 'influence_level']).size().unstack()
influence_pct = influence_counts.div(influence_counts.sum(axis=1), axis=0)
influence_pct.T.plot(kind='bar', ax=axes[1,1], color=['#e74c3c', '#3498db'])
axes[1,1].set_title('Influence Level Distribution by Risk Status')
axes[1,1].set_ylabel('Proportion')
axes[1,1].legend(title='Engagement Risk')
axes[1,1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('/work/fig4_stakeholder_patterns.png', dpi=150, bbox_inches='tight')
plt.close()
print("Figure 4 saved.")

print("\nAll figures generated successfully.")