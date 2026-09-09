import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the data
issue_agg = db.frame(db.query("SELECT project_name, COUNT(*) as total_issues, SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END)*1.0/COUNT(*) as bug_rate, AVG(regression_ratio) as avg_regression_ratio, AVG(lifecycle_quality_score) as avg_lifecycle_quality, AVG(lifecycle_deviation_ratio) as avg_deviation_ratio, AVG(total_risk_score) as avg_risk_score, AVG(completion_probability) as avg_completion_prob, AVG(intelligence_score) as avg_intelligence, SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate, SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate, SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate, SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate, SUM(CASE WHEN high_complexity_risk=1 THEN 1 ELSE 0 END)*1.0/COUNT(*) as high_complexity_rate, COUNT(DISTINCT assignee_name) as distinct_assignees, SUM(CASE WHEN assignment_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as assignment_risk_rate, SUM(CASE WHEN engagement_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as engagement_risk_rate, SUM(CASE WHEN age_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as age_risk_rate, SUM(CASE WHEN process_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as process_risk_rate, SUM(CASE WHEN deviation_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as deviation_risk_rate, SUM(CASE WHEN complexity_risk_score > 0 THEN 1 ELSE 0 END)*1.0/COUNT(*) as complexity_risk_rate FROM jira__issue_intelligence_analytics GROUP BY project_name"))

proj_agg = db.frame(db.query("SELECT project_name, AVG(avg_close_time_days) as avg_close_time, MIN(avg_close_time_days) as min_close_time, MAX(avg_close_time_days) as max_close_time, SUM(count_closed_issues) as total_closed_issues, SUM(count_open_issues) as total_open_issues, AVG(avg_age_currently_open_days) as avg_age_open, AVG(median_close_time_days) as avg_median_close FROM jira__project_enhanced GROUP BY project_name"))

team_agg = db.frame(db.query("SELECT project_name, COUNT(*) as team_size, SUM(at_churn_risk) as churn_risk_count, SUM(inactive_recently) as inactive_count, AVG(consistency_percentage) as avg_consistency, AVG(resolution_rate_percentage) as avg_resolution_rate, AVG(overall_performance_score) as avg_performance, AVG(avg_sprint_completion_rate) as avg_sprint_completion, AVG(days_since_first_issue) as avg_tenure_days, AVG(estimate_accuracy_percentage) as avg_estimate_accuracy FROM jira__team_performance_dashboard GROUP BY project_name"))

# Merge datasets
merged = issue_agg.merge(proj_agg, on='project_name', how='inner')
merged_all = merged.merge(team_agg, on='project_name', how='left')

print("Columns:", merged_all.columns.tolist())
print("Shape:", merged_all.shape)
print("\nProjects with avg_close_time < 15:")
fast = merged_all[merged_all['avg_close_time'] < 15]
print(fast[['project_name', 'avg_close_time', 'team_size', 'churn_risk_count', 'bug_rate', 'avg_regression_ratio', 'avg_lifecycle_quality', 'unusually_fast_rate', 'stat_outlier_rate', 'blocked_rate', 'avg_risk_score', 'avg_intelligence', 'avg_consistency']].to_string())

print("\n\nSlow projects (avg_close_time >= 40):")
slow = merged_all[merged_all['avg_close_time'] >= 40]
print(slow[['project_name', 'avg_close_time', 'team_size', 'churn_risk_count', 'bug_rate', 'avg_regression_ratio', 'avg_lifecycle_quality', 'unusually_fast_rate', 'stat_outlier_rate', 'blocked_rate', 'avg_risk_score', 'avg_intelligence', 'avg_consistency']].head(20).to_string())

# Compute correlations
print("\n\nCorrelation with avg_close_time:")
corr_cols = ['bug_rate', 'avg_regression_ratio', 'avg_lifecycle_quality', 'avg_deviation_ratio', 
             'avg_risk_score', 'avg_completion_prob', 'avg_intelligence', 'unusually_fast_rate', 
             'stat_outlier_rate', 'above_normal_rate', 'blocked_rate', 'high_complexity_rate',
             'assignment_risk_rate', 'engagement_risk_rate', 'age_risk_rate', 'process_risk_rate',
             'deviation_risk_rate', 'complexity_risk_rate', 'avg_age_open', 'total_closed_issues']
for col in corr_cols:
    if col in merged_all.columns:
        r, p = stats.pearsonr(merged_all['avg_close_time'].dropna(), merged_all[col].dropna())
        print(f"  {col}: r={r:.4f}, p={p:.6f}")

# Also compute team stability for the 5 projects with team data
print("\n\nTeam Stability Analysis:")
for _, row in merged_all.dropna(subset=['team_size']).iterrows():
    stability = 100 * (1 - row['churn_risk_count'] / row['team_size'])
    # Weighted stability combining churn and consistency
    weighted_stability = stability * (row['avg_consistency'] / 100) if pd.notna(row['avg_consistency']) else stability
    print(f"  {row['project_name']}: team_size={row['team_size']}, churn_risk={row['churn_risk_count']}, stability={stability:.1f}%, weighted_stability={weighted_stability:.1f}%, avg_close={row['avg_close_time']:.0f}d")

# Create visualizations
plt.rcParams['figure.figsize'] = (14, 10)
sns.set_style("whitegrid")

# 1. Bug rate vs avg_close_time
fig, axes = plt.subplots(2, 3, figsize=(16, 10))
ax1 = axes[0, 0]
ax1.scatter(merged_all['avg_close_time'], merged_all['bug_rate'], alpha=0.6, c='steelblue')
# Highlight fast projects
for _, row in merged_all[merged_all['avg_close_time'] < 15].iterrows():
    ax1.scatter(row['avg_close_time'], row['bug_rate'], color='red', s=80, zorder=5)
ax1.set_xlabel('Average Close Time (days)')
ax1.set_ylabel('Bug Rate')
ax1.set_title('Bug Rate vs Project Speed')

# 2. Regression ratio vs avg_close_time
ax2 = axes[0, 1]
ax2.scatter(merged_all['avg_close_time'], merged_all['avg_regression_ratio'], alpha=0.6, c='steelblue')
for _, row in merged_all[merged_all['avg_close_time'] < 15].iterrows():
    ax2.scatter(row['avg_close_time'], row['avg_regression_ratio'], color='red', s=80, zorder=5)
ax2.set_xlabel('Average Close Time (days)')
ax2.set_ylabel('Avg Regression Ratio')
ax2.set_title('Regression Ratio vs Project Speed')

# 3. Lifecycle quality vs avg_close_time
ax3 = axes[0, 2]
ax3.scatter(merged_all['avg_close_time'], merged_all['avg_lifecycle_quality'], alpha=0.6, c='steelblue')
for _, row in merged_all[merged_all['avg_close_time'] < 15].iterrows():
    ax3.scatter(row['avg_close_time'], row['avg_lifecycle_quality'], color='red', s=80, zorder=5)
ax3.set_xlabel('Average Close Time (days)')
ax3.set_ylabel('Avg Lifecycle Quality Score')
ax3.set_title('Lifecycle Quality vs Project Speed')

# 4. Unusually Fast rate vs avg_close_time
ax4 = axes[1, 0]
ax4.scatter(merged_all['avg_close_time'], merged_all['unusually_fast_rate'], alpha=0.6, c='steelblue')
for _, row in merged_all[merged_all['avg_close_time'] < 15].iterrows():
    ax4.scatter(row['avg_close_time'], row['unusually_fast_rate'], color='red', s=80, zorder=5)
ax4.set_xlabel('Average Close Time (days)')
ax4.set_ylabel('Unusually Fast Rate')
ax4.set_title('Unusually Fast Rate vs Project Speed')

# 5. Blocked rate vs avg_close_time
ax5 = axes[1, 1]
ax5.scatter(merged_all['avg_close_time'], merged_all['blocked_rate'], alpha=0.6, c='steelblue')
for _, row in merged_all[merged_all['avg_close_time'] < 15].iterrows():
    ax5.scatter(row['avg_close_time'], row['blocked_rate'], color='red', s=80, zorder=5)
ax5.set_xlabel('Average Close Time (days)')
ax5.set_ylabel('Blocked Rate')
ax5.set_title('Blocked Issues Rate vs Project Speed')

# 6. Risk score vs avg_close_time
ax6 = axes[1, 2]
ax6.scatter(merged_all['avg_close_time'], merged_all['avg_risk_score'], alpha=0.6, c='steelblue')
for _, row in merged_all[merged_all['avg_close_time'] < 15].iterrows():
    ax6.scatter(row['avg_close_time'], row['avg_risk_score'], color='red', s=80, zorder=5)
ax6.set_xlabel('Average Close Time (days)')
ax6.set_ylabel('Avg Risk Score')
ax6.set_title('Risk Score vs Project Speed')

plt.tight_layout()
plt.savefig('/work/quality_metrics_vs_speed.png', dpi=150)
plt.close()

# Comparison: Fast vs Other projects
fast_projects = merged_all[merged_all['avg_close_time'] < 15].copy()
other_projects = merged_all[merged_all['avg_close_time'] >= 15].copy()

print("\n\n=== Fast Projects (avg_close < 15d) vs Others ===")
metrics_to_compare = ['bug_rate', 'avg_regression_ratio', 'avg_lifecycle_quality', 
                      'unusually_fast_rate', 'stat_outlier_rate', 'above_normal_rate',
                      'blocked_rate', 'avg_risk_score', 'avg_intelligence', 'avg_deviation_ratio',
                      'engagement_risk_rate', 'age_risk_rate', 'process_risk_rate']

for metric in metrics_to_compare:
    f_mean = fast_projects[metric].mean()
    o_mean = other_projects[metric].mean()
    f_std = fast_projects[metric].std()
    o_std = other_projects[metric].std()
    # T-test
    t_stat, p_val = stats.ttest_ind(fast_projects[metric].dropna(), other_projects[metric].dropna())
    direction = "HIGHER" if f_mean > o_mean else "LOWER"
    sig = "SIGNIFICANT" if p_val < 0.05 else "not significant"
    print(f"  {metric}: Fast={f_mean:.4f}±{f_std:.4f}, Others={o_mean:.4f}±{o_std:.4f} ({direction}, p={p_val:.4f}, {sig})")

# Long-term sustainability analysis
# Look at indicators of burnout/churn risk
print("\n\n=== Long-term Sustainability Indicators ===")
# For projects with team data, compare fast vs slow
team_data = merged_all.dropna(subset=['team_size'])
print("Projects with team data:")
for _, row in team_data.iterrows():
    churn_pct = row['churn_risk_count'] / row['team_size'] * 100
    stability = 100 - churn_pct
    print(f"  {row['project_name']}: avg_close={row['avg_close_time']:.0f}d, stability={stability:.1f}%, churn%={churn_pct:.1f}%, team_size={row['team_size']:.0f}, consistency={row['avg_consistency']:.1f}%, performance={row['avg_performance']:.0f}")

# Bar chart comparing fast vs slow project quality
fig, ax = plt.subplots(figsize=(12, 6))
comparison_metrics = ['bug_rate', 'avg_regression_ratio', 'blocked_rate', 'unusually_fast_rate', 'stat_outlier_rate']
x = np.arange(len(comparison_metrics))
width = 0.35

fast_means = [fast_projects[m].mean() for m in comparison_metrics]
other_means = [other_projects[m].mean() for m in comparison_metrics]

bars1 = ax.bar(x - width/2, fast_means, width, label='Fast Projects (<15d)', color='coral', alpha=0.8)
bars2 = ax.bar(x + width/2, other_means, width, label='Other Projects (>=15d)', color='steelblue', alpha=0.8)

ax.set_ylabel('Rate')
ax.set_title('Quality Indicators: Fast vs Other Projects')
ax.set_xticks(x)
ax.set_xticklabels(['Bug Rate', 'Regression Ratio', 'Blocked Rate', 'Unusually Fast Rate', 'Statistical Outlier Rate'], rotation=20)
ax.legend()
plt.tight_layout()
plt.savefig('/work/fast_vs_other_quality.png', dpi=150)
plt.close()

# Team stability bar chart
fig, ax = plt.subplots(figsize=(10, 6))
team_names = team_data['project_name'].tolist()
team_stability = [100 * (1 - row['churn_risk_count']/row['team_size']) for _, row in team_data.iterrows()]
team_close = team_data['avg_close_time'].tolist()
team_consistency = team_data['avg_consistency'].tolist()

colors = ['coral' if c < 15 else 'steelblue' for c in team_close]
bars = ax.bar(team_names, team_stability, color=colors, alpha=0.8)
ax.set_ylabel('Team Stability (%)')
ax.set_title('Team Stability by Project (Redefined: 100% - Churn Risk %)')
ax.set_ylim(0, 105)
for bar, stab, close, cons in zip(bars, team_stability, team_close, team_consistency):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
            f'{stab:.0f}%', ha='center', va='bottom', fontsize=9)
    ax.text(bar.get_x() + bar.get_width()/2, 5, 
            f'close={close:.0f}d\nconsist={cons:.0f}%', ha='center', va='bottom', fontsize=8, color='white')
plt.tight_layout()
plt.savefig('/work/team_stability_by_project.png', dpi=150)
plt.close()

print("\n\nAnalysis complete. Files saved.")