import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

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

# Cluster (already computed in previous run, but recompute here)
X = proj_df[['health_risk_score', 'schedule_risk_score', 'resource_risk_score', 
             'complexity_risk_score', 'scope_risk_score']].values
means = X.mean(axis=0)
stds = X.std(axis=0)
X_scaled = (X - means) / stds
Z = linkage(X_scaled, method='ward')
clusters = fcluster(Z, 3, criterion='maxclust')
proj_df['cluster'] = clusters

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

# 2. Risk sub-score boxplot - use positions instead of labels param
ax = axes[0, 1]
risk_data = [proj_df['health_risk_score'], proj_df['schedule_risk_score'], 
             proj_df['resource_risk_score'], proj_df['complexity_risk_score'], 
             proj_df['scope_risk_score']]
labels_list = ['Health', 'Schedule', 'Resource', 'Complexity', 'Scope']
bp = ax.boxplot(risk_data, patch_artist=True)
for patch, color in zip(bp['boxes'], ['lightblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightyellow']):
    patch.set_facecolor(color)
ax.set_xticklabels(labels_list)
ax.set_ylabel('Risk Score')
ax.set_title('Risk Sub-Score Distributions')

# 3. Complexity vs total risk scatter
ax = axes[1, 0]
scatter = ax.scatter(proj_df['complexity_risk_score'], proj_df['total_risk_score'], 
                     c=proj_df['success_probability'], cmap='viridis', alpha=0.7, s=40)
ax.set_xlabel('Complexity Risk Score')
ax.set_ylabel('Total Risk Score')
ax.set_title('Complexity vs Total Risk (colored by Success Probability)')
plt.colorbar(scatter, ax=ax, label='Success Probability')

# 4. Cluster visualization
ax = axes[1, 1]
colors_map = {1: 'red', 2: 'blue', 3: 'green'}
for c in sorted(proj_df['cluster'].unique()):
    mask = proj_df['cluster'] == c
    ax.scatter(proj_df.loc[mask, 'health_risk_score'], proj_df.loc[mask, 'schedule_risk_score'], 
               c=colors_map[c], label=f'Cluster {c}', alpha=0.6, s=30)
ax.set_xlabel('Health Risk Score')
ax.set_ylabel('Schedule Risk Score')
ax.set_title('Project Risk Profile Clusters (Health vs Schedule)')
ax.legend()

plt.tight_layout()
plt.savefig('/work/project_analysis.png', dpi=150)
print("Saved figure to /work/project_analysis.png")

# Also get stakeholder data  
res2 = db.query("SELECT direct_network_connections, total_projects_involved, "
                "cross_functional_projects, engagement_breadth_score, "
                "engagement_quality_score, engagement_impact_score, "
                "total_engagement_score, strategic_value_score, "
                "total_outbound_influence, total_inbound_influence, "
                "stakeholder_archetype, influence_level, engagement_risk_status "
                "FROM jira__stakeholder_engagement_insights")
stake_df = db.frame(res2)

# Correlation summary
print("\n=== KEY CORRELATIONS ===")
from scipy import stats
r1, p1 = stats.pearsonr(stake_df['direct_network_connections'], stake_df['cross_functional_projects'])
r2, p2 = stats.pearsonr(stake_df['direct_network_connections'], stake_df['total_engagement_score'])
r3, p3 = stats.pearsonr(stake_df['direct_network_connections'], stake_df['engagement_breadth_score'])
r4, p4 = stats.pearsonr(stake_df['direct_network_connections'], stake_df['total_outbound_influence'])
print(f"Connections vs Cross-functional Projects: r={r1:.4f}, p={p1:.2e}")
print(f"Connections vs Total Engagement Score: r={r2:.4f}, p={p2:.2e}")
print(f"Connections vs Engagement Breadth: r={r3:.4f}, p={r3:.2e}")
print(f"Connections vs Outbound Influence: r={r4:.4f}, p={p4:.2e}")

# Print key stats for the report
print(f"\n=== REPORT STATS ===")
print(f"Stakeholders: {len(stake_df)}")
print(f"Projects: {len(proj_df)}")
print(f"Connection range: {stake_df['direct_network_connections'].min()}-{stake_df['direct_network_connections'].max()}")
print(f"Connection median: {stake_df['direct_network_connections'].median():.0f}")
print(f"Connection IQR: {stake_df['direct_network_connections'].quantile(0.25):.0f}-{stake_df['direct_network_connections'].quantile(0.75):.0f}")
print(f"Complexity risk range: {proj_df['complexity_risk_score'].min()}-{proj_df['complexity_risk_score'].max()}")
print(f"Complexity risk median: {proj_df['complexity_risk_score'].median():.0f}")
print(f"Success probability median: {proj_df['success_probability'].median():.3f}")
print(f"Corr(complexity_risk, success_prob): {proj_df['complexity_risk_score'].corr(proj_df['success_probability']):.4f}")
print(f"High-conn stakeholders (>=21): {(stake_df['direct_network_connections'] >= 21).sum()} / {len(stake_df)}")
print(f"High-conn stakeholders in Low Risk: {(stake_df[(stake_df['direct_network_connections'] >= 21) & (stake_df['engagement_risk_status'] == 'Low Risk')]).shape[0]}")