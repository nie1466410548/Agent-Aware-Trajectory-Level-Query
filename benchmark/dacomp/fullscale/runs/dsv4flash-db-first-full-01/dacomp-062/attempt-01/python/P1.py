import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import json

# Get stakeholder numeric columns
res = db.query("SELECT direct_network_connections, total_projects_involved, cross_functional_projects, "
               "engagement_breadth_score, engagement_depth_score, engagement_quality_score, "
               "engagement_impact_score, total_engagement_score, strategic_value_score, "
               "total_outbound_influence, total_inbound_influence, avg_outbound_influence_strength "
               "FROM jira__stakeholder_engagement_insights")
stake_df = db.frame(res)
print("Stakeholder rows:", len(stake_df))

# Get project numeric columns
res2 = db.query("SELECT complexity_risk_score, success_probability, overall_health_score, "
                "total_risk_score, health_risk_score, schedule_risk_score, resource_risk_score, "
                "scope_risk_score, value_delivery_percentage, team_stability_percentage, "
                "total_hours_invested, estimated_project_value_points, delivered_value_points, "
                "sprint_adoption_rate, unique_issue_types, unique_components, total_external_links "
                "FROM jira__project_risk_assessment")
proj_df = db.frame(res2)
print("Project rows:", len(proj_df))

# --- Stakeholder correlations ---
print("\n=== STAKEHOLDER: Correlation with direct_network_connections ===")
conn_col = 'direct_network_connections'
for col in stake_df.columns:
    if col == conn_col:
        continue
    r, p = stats.pearsonr(stake_df[conn_col], stake_df[col])
    print(f"  {conn_col} vs {col}: r={r:.4f}, p={p:.2e}")

# --- Project correlations ---
print("\n=== PROJECT: Correlation with complexity_risk_score ===")
comp_col = 'complexity_risk_score'
for col in proj_df.columns:
    if col == comp_col:
        continue
    r, p = stats.pearsonr(proj_df[comp_col], proj_df[col])
    print(f"  {comp_col} vs {col}: r={r:.4f}, p={p:.2e}")

print("\n=== PROJECT: Correlation with success_probability ===")
sp_col = 'success_probability'
for col in proj_df.columns:
    if col == sp_col:
        continue
    r, p = stats.pearsonr(proj_df[sp_col], proj_df[col])
    print(f"  {sp_col} vs {col}: r={r:.4f}, p={p:.2e}")

# --- Complexity vs Success ---
r_cs, p_cs = stats.pearsonr(proj_df['complexity_risk_score'], proj_df['success_probability'])
print(f"\n  complexity_risk_score vs success_probability: r={r_cs:.4f}, p={p_cs:.2e}")

# --- Quantiles for stakeholder connections ---
print("\n=== STAKEHOLDER: direct_network_connections quantiles ===")
for q in [0, 10, 25, 50, 75, 90, 100]:
    val = np.percentile(stake_df['direct_network_connections'], q)
    print(f"  {q}th percentile: {val}")

# --- Quantiles for project metrics ---
print("\n=== PROJECT: complexity_risk_score quantiles ===")
for q in [0, 10, 25, 50, 75, 90, 100]:
    val = np.percentile(proj_df['complexity_risk_score'], q)
    print(f"  {q}th percentile: {val}")

print("\n=== PROJECT: success_probability quantiles ===")
for q in [0, 10, 25, 50, 75, 90, 100]:
    val = np.percentile(proj_df['success_probability'], q)
    print(f"  {q}th percentile: {val}")

# --- Create visualizations ---
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. Stakeholder: connection histogram
ax = axes[0, 0]
ax.hist(stake_df['direct_network_connections'], bins=40, color='steelblue', edgecolor='white', alpha=0.8)
ax.axvline(np.median(stake_df['direct_network_connections']), color='red', linestyle='--', label=f"Median: {np.median(stake_df['direct_network_connections']):.0f}")
ax.axvline(np.mean(stake_df['direct_network_connections']), color='orange', linestyle='--', label=f"Mean: {np.mean(stake_df['direct_network_connections']):.1f}")
ax.set_xlabel('Direct Network Connections')
ax.set_ylabel('Count')
ax.set_title('Distribution of Stakeholder Network Connections')
ax.legend()

# 2. Project: complexity risk histogram
ax = axes[0, 1]
ax.hist(proj_df['complexity_risk_score'], bins=20, color='salmon', edgecolor='white', alpha=0.8)
ax.axvline(np.median(proj_df['complexity_risk_score']), color='red', linestyle='--', label=f"Median: {np.median(proj_df['complexity_risk_score']):.0f}")
ax.axvline(np.mean(proj_df['complexity_risk_score']), color='orange', linestyle='--', label=f"Mean: {np.mean(proj_df['complexity_risk_score']):.1f}")
ax.set_xlabel('Complexity Risk Score')
ax.set_ylabel('Count')
ax.set_title('Distribution of Project Complexity Risk')
ax.legend()

# 3. Project: success probability histogram
ax = axes[0, 2]
ax.hist(proj_df['success_probability'], bins=20, color='lightgreen', edgecolor='white', alpha=0.8)
ax.axvline(np.median(proj_df['success_probability']), color='red', linestyle='--', label=f"Median: {np.median(proj_df['success_probability']):.3f}")
ax.axvline(np.mean(proj_df['success_probability']), color='orange', linestyle='--', label=f"Mean: {np.mean(proj_df['success_probability']):.3f}")
ax.set_xlabel('Success Probability')
ax.set_ylabel('Count')
ax.set_title('Distribution of Project Success Probability')
ax.legend()

# 4. Scatter: complexity vs success
ax = axes[1, 0]
ax.scatter(proj_df['complexity_risk_score'], proj_df['success_probability'], 
           c='purple', alpha=0.5, s=30)
ax.set_xlabel('Complexity Risk Score')
ax.set_ylabel('Success Probability')
ax.set_title(f'Complexity Risk vs Success Probability\nr={r_cs:.4f}, p={p_cs:.2e}')
# Add trend line
m, b = np.polyfit(proj_df['complexity_risk_score'], proj_df['success_probability'], 1)
ax.plot(proj_df['complexity_risk_score'], m*proj_df['complexity_risk_score'] + b, 
        color='red', linestyle='--', linewidth=1)

# 5. Stakeholder: connections vs engagement score
ax = axes[1, 1]
r_conn_eng, _ = stats.pearsonr(stake_df['direct_network_connections'], stake_df['total_engagement_score'])
ax.scatter(stake_df['direct_network_connections'], stake_df['total_engagement_score'], 
           c='teal', alpha=0.3, s=5)
ax.set_xlabel('Direct Network Connections')
ax.set_ylabel('Total Engagement Score')
ax.set_title(f'Connections vs Engagement Score\nr={r_conn_eng:.4f}')

# 6. Stakeholder: connections vs cross-functional projects
ax = axes[1, 2]
r_conn_cross, _ = stats.pearsonr(stake_df['direct_network_connections'], stake_df['cross_functional_projects'])
ax.scatter(stake_df['direct_network_connections'], stake_df['cross_functional_projects'], 
           c='coral', alpha=0.3, s=5)
ax.set_xlabel('Direct Network Connections')
ax.set_ylabel('Cross-Functional Projects')
ax.set_title(f'Connections vs Cross-Functional Projects\nr={r_conn_cross:.4f}')

plt.tight_layout()
plt.savefig('/work/analysis_plots.png', dpi=150)
print("\nSaved figure to /work/analysis_plots.png")