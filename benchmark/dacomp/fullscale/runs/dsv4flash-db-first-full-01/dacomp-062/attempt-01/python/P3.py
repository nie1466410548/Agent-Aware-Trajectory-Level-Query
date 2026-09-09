import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Get project data
res = db.query("SELECT complexity_risk_score, success_probability, overall_health_score, "
               "total_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, "
               "scope_risk_score, value_delivery_percentage, team_stability_percentage, "
               "total_hours_invested, estimated_project_value_points, delivered_value_points, "
               "sprint_adoption_rate, unique_issue_types, unique_components, total_external_links, "
               "net_issue_growth_30d, resolution_velocity_change_percent, "
               "trajectory_status, risk_category, primary_risk_factor, primary_risk_driver "
               "FROM jira__project_risk_assessment")
proj_df = db.frame(res)
print(f"Project rows: {len(proj_df)}")

# Success probability distribution
print("\n=== Success probability detailed distribution ===")
print(f"  Min: {proj_df['success_probability'].min():.3f}")
print(f"  25th: {proj_df['success_probability'].quantile(0.25):.3f}")
print(f"  Median: {proj_df['success_probability'].median():.3f}")
print(f"  75th: {proj_df['success_probability'].quantile(0.75):.3f}")
print(f"  Max: {proj_df['success_probability'].max():.3f}")
print(f"  Std: {proj_df['success_probability'].std():.4f}")
print(f"  Unique success_probability values: {proj_df['success_probability'].nunique()}")
print(f"  Projects with success_probability >= 0.90: {(proj_df['success_probability'] >= 0.90).sum()} / {len(proj_df)}")
print(f"  Projects with success_probability >= 0.95: {(proj_df['success_probability'] >= 0.95).sum()} / {len(proj_df)}")

# Risk sub-score correlation matrix
risk_cols = ['complexity_risk_score', 'health_risk_score', 'schedule_risk_score', 
             'resource_risk_score', 'scope_risk_score', 'total_risk_score', 'success_probability']
print("\n=== Risk sub-score correlation matrix ===")
corr = proj_df[risk_cols].corr()
print(corr.round(3))

# Check total_risk_score composition
print("\n=== Total risk = sum of sub-scores? ===")
proj_df['sum_sub_scores'] = (proj_df['health_risk_score'] + proj_df['schedule_risk_score'] + 
                              proj_df['resource_risk_score'] + proj_df['complexity_risk_score'] + 
                              proj_df['scope_risk_score'])
print(f"  Max |total_risk - sum|: {(proj_df['total_risk_score'] - proj_df['sum_sub_scores']).abs().max()}")
print(f"  Corr(total_risk, sum_sub_scores): {proj_df['total_risk_score'].corr(proj_df['sum_sub_scores']):.4f}")

# Manual hierarchical clustering
X = proj_df[['health_risk_score', 'schedule_risk_score', 'resource_risk_score', 
             'complexity_risk_score', 'scope_risk_score']].values
# Standardize manually
means = X.mean(axis=0)
stds = X.std(axis=0)
X_scaled = (X - means) / stds

# Use scipy's linkage for hierarchical clustering
Z = linkage(X_scaled, method='ward')
# Cut at 3 clusters
clusters = fcluster(Z, 3, criterion='maxclust')
proj_df['cluster'] = clusters

print("\n=== Project cluster characteristics ===")
for c in sorted(proj_df['cluster'].unique()):
    subset = proj_df[proj_df['cluster'] == c]
    print(f"\nCluster {c} (n={len(subset)}):")
    print(f"  Avg complexity: {subset['complexity_risk_score'].mean():.1f}")
    print(f"  Avg success_prob: {subset['success_probability'].mean():.3f}")
    print(f"  Avg health_risk: {subset['health_risk_score'].mean():.1f}")
    print(f"  Avg schedule_risk: {subset['schedule_risk_score'].mean():.1f}")
    print(f"  Avg resource_risk: {subset['resource_risk_score'].mean():.1f}")
    print(f"  Avg scope_risk: {subset['scope_risk_score'].mean():.1f}")
    print(f"  Avg total_risk: {subset['total_risk_score'].mean():.1f}")
    print(f"  Trajectory: {subset['trajectory_status'].value_counts().to_dict()}")
    print(f"  Risk category: {subset['risk_category'].value_counts().to_dict()}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 1. Success probability distribution
ax = axes[0, 0]
bins = np.linspace(0.45, 0.96, 30)
ax.hist(proj_df['success_probability'], bins=bins, color='lightgreen', edgecolor='white', alpha=0.8)
ax.axvline(proj_df['success_probability'].median(), color='red', linestyle='--', 
           label=f"Median: {proj_df['success_probability'].median():.3f}")
ax.axvline(proj_df['success_probability'].mean(), color='orange', linestyle='--', 
           label=f"Mean: {proj_df['success_probability'].mean():.3f}")
ax.set_xlabel('Success Probability')
ax.set_ylabel('Count')
ax.set_title('Project Success Probability Distribution')
ax.legend()

# 2. Risk sub-score boxplot
ax = axes[0, 1]
risk_data = [proj_df['health_risk_score'], proj_df['schedule_risk_score'], 
             proj_df['resource_risk_score'], proj_df['complexity_risk_score'], 
             proj_df['scope_risk_score']]
labels = ['Health', 'Schedule', 'Resource', 'Complexity', 'Scope']
bp = ax.boxplot(risk_data, labels=labels, patch_artist=True)
colors = ['lightblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightyellow']
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
ax.set_ylabel('Risk Score')
ax.set_title('Risk Sub-Score Distributions')
ax.tick_params(axis='x', rotation=30)

# 3. Complexity vs total risk scatter
ax = axes[1, 0]
scatter = ax.scatter(proj_df['complexity_risk_score'], proj_df['total_risk_score'], 
                     c=proj_df['success_probability'], cmap='viridis', alpha=0.7, s=40)
ax.set_xlabel('Complexity Risk Score')
ax.set_ylabel('Total Risk Score')
ax.set_title('Complexity vs Total Risk\n(colored by Success Probability)')
plt.colorbar(scatter, ax=ax, label='Success Probability')

# 4. Manual 2D projection using first two risk dimensions
ax = axes[1, 1]
# Use health_risk and schedule_risk as the two most explanatory dimensions
colors_map = {1: 'red', 2: 'blue', 3: 'green'}
for c in sorted(proj_df['cluster'].unique()):
    mask = proj_df['cluster'] == c
    ax.scatter(proj_df.loc[mask, 'health_risk_score'], proj_df.loc[mask, 'schedule_risk_score'], 
               c=colors_map[c], label=f'Cluster {c}', alpha=0.6, s=30)
ax.set_xlabel('Health Risk Score')
ax.set_ylabel('Schedule Risk Score')
ax.set_title('Project Risk Profile Clusters\n(Health vs Schedule Risk)')
ax.legend()

plt.tight_layout()
plt.savefig('/work/project_analysis.png', dpi=150)
print("\nSaved figure to /work/project_analysis.png")

# Also get top stakeholder data for a combined view
res2 = db.query("SELECT direct_network_connections, total_projects_involved, "
                "cross_functional_projects, engagement_breadth_score, "
                "engagement_quality_score, engagement_impact_score, "
                "total_engagement_score, strategic_value_score, "
                "total_outbound_influence, total_inbound_influence, "
                "stakeholder_archetype, influence_level, engagement_risk_status "
                "FROM jira__stakeholder_engagement_insights")
stake_df = db.frame(res2)

# Print summary stats for report
print("\n\n=== KEY STATISTICS FOR REPORT ===")
print(f"Stakeholders: {len(stake_df)}")
print(f"Projects: {len(proj_df)}")
print(f"Stakeholder connection range: {stake_df['direct_network_connections'].min()} - {stake_df['direct_network_connections'].max()}")
print(f"Stakeholder connection median: {stake_df['direct_network_connections'].median()}")
print(f"Project complexity risk range: {proj_df['complexity_risk_score'].min()} - {proj_df['complexity_risk_score'].max()}")
print(f"Project success probability median: {proj_df['success_probability'].median():.3f}")
print(f"Correlation(complexity, success): {proj_df['complexity_risk_score'].corr(proj_df['success_probability']):.4f}")
print(f"Correlation(connections, cross_func): {stake_df['direct_network_connections'].corr(stake_df['cross_functional_projects']):.4f}")
print(f"Correlation(connections, engagement): {stake_df['direct_network_connections'].corr(stake_df['total_engagement_score']):.4f}")
print(f"Correlation(connections, breadth): {stake_df['direct_network_connections'].corr(stake_df['engagement_breadth_score']):.4f}")
print(f"Correlation(connections, influence): {stake_df['direct_network_connections'].corr(stake_df['total_outbound_influence']):.4f}")