import numpy as np
import pandas as pd
from scipy import stats
from scipy.cluster.hierarchy import linkage, fcluster
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Get project data for deeper analysis
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
val_counts = proj_df['success_probability'].value_counts().sort_index()
print(f"  Top success probabilities:")
for val, cnt in val_counts.head(10).items():
    print(f"    {val:.3f}: {cnt} projects")

# Check if success_probability is largely constant
unique_vals = proj_df['success_probability'].nunique()
print(f"\n  Unique success_probability values: {unique_vals}")
print(f"  Projects with success_probability >= 0.90: {(proj_df['success_probability'] >= 0.90).sum()} / {len(proj_df)}")
print(f"  Projects with success_probability >= 0.95: {(proj_df['success_probability'] >= 0.95).sum()} / {len(proj_df)}")

# Risk sub-score correlations
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
print(f"  Max difference: {(proj_df['total_risk_score'] - proj_df['sum_sub_scores']).abs().max()}")

# Check if there are clusters of projects by risk profiles
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Use risk sub-scores for clustering
X = proj_df[['health_risk_score', 'schedule_risk_score', 'resource_risk_score', 
             'complexity_risk_score', 'scope_risk_score']].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)
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

# Create additional visualization
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
for patch, color in zip(bp['boxes'], ['lightblue', 'lightcoral', 'lightgreen', 'lightsalmon', 'lightyellow']):
    patch.set_facecolor(color)
ax.set_ylabel('Risk Score')
ax.set_title('Risk Sub-Score Distributions')
ax.tick_params(axis='x', rotation=30)

# 3. Scatter matrix of key risk variables
ax = axes[1, 0]
scatter = ax.scatter(proj_df['complexity_risk_score'], proj_df['total_risk_score'], 
                     c=proj_df['success_probability'], cmap='viridis', alpha=0.7, s=40)
ax.set_xlabel('Complexity Risk Score')
ax.set_ylabel('Total Risk Score')
ax.set_title('Complexity vs Total Risk\n(colored by Success Probability)')
plt.colorbar(scatter, ax=ax, label='Success Probability')

# 4. Cluster visualization (first 2 PCA components)
from sklearn.decomposition import PCA
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
ax = axes[1, 1]
colors = ['red', 'blue', 'green']
for c in sorted(proj_df['cluster'].unique()):
    mask = proj_df['cluster'] == c
    ax.scatter(X_pca[mask, 0], X_pca[mask, 1], c=colors[c], label=f'Cluster {c}', alpha=0.6, s=30)
ax.set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%} variance)')
ax.set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%} variance)')
ax.set_title('Project Risk Profile Clusters (PCA)')
ax.legend()

plt.tight_layout()
plt.savefig('/work/project_analysis.png', dpi=150)
print("\nSaved figure to /work/project_analysis.png")

# Print PCA loadings
print("\n=== PCA loadings ===")
loadings = pd.DataFrame(
    pca.components_.T,
    columns=['PC1', 'PC2'],
    index=['health_risk', 'schedule_risk', 'resource_risk', 'complexity_risk', 'scope_risk']
)
print(loadings.round(3))