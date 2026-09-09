import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Get individual project instances with avg_close_time < 15
fast_instances = db.frame(db.query("""
    SELECT project_id, project_name, project_key, project_lead_user_name, 
           avg_close_time_days, median_close_time_days, count_closed_issues, count_open_issues,
           avg_age_currently_open_days, avg_assigned_close_time_days
    FROM jira__project_enhanced 
    WHERE avg_close_time_days < 15
    ORDER BY avg_close_time_days
"""))
print("=== Fast Project Instances (avg_close_time_days < 15) ===")
print(fast_instances.to_string())

# Get the issue-level breakdown for the two fast project names
print("\n\n=== Issue-level metrics for Data Analytics Delta ===")
dad_issues = db.frame(db.query("""
    SELECT 
        issue_type,
        COUNT(*) as cnt,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(total_lifecycle_days) as avg_lifecycle_days,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        AVG(total_risk_score) as avg_risk
    FROM jira__issue_intelligence_analytics 
    WHERE project_name = 'Data Analytics Delta'
    GROUP BY issue_type
    ORDER BY cnt DESC
"""))
print(dad_issues.to_string())

print("\n\n=== Issue-level metrics for Mobile App Delta ===")
mad_issues = db.frame(db.query("""
    SELECT 
        issue_type,
        COUNT(*) as cnt,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(total_lifecycle_days) as avg_lifecycle_days,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        AVG(total_risk_score) as avg_risk
    FROM jira__issue_intelligence_analytics 
    WHERE project_name = 'Mobile App Delta'
    GROUP BY issue_type
    ORDER BY cnt DESC
"""))
print(mad_issues.to_string())

# Get overall averages for comparison
print("\n\n=== Overall averages ===")
overall = db.frame(db.query("""
    SELECT 
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        AVG(total_risk_score) as avg_risk,
        AVG(intelligence_score) as avg_intel,
        AVG(completion_probability) as avg_cp
    FROM jira__issue_intelligence_analytics
"""))
print(overall.to_string())

# Compare specific metrics for fast projects vs slow projects
# Get per-project_name regression and lifecycle quality data
proj_data = db.frame(db.query("""
    SELECT project_name,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        AVG(total_risk_score) as avg_risk,
        AVG(intelligence_score) as avg_intel,
        AVG(completion_probability) as avg_cp,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END)*1.0/COUNT(*) as bug_rate
    FROM jira__issue_intelligence_analytics
    GROUP BY project_name
"""))

# Join with project_enhanced
proj_enhanced = db.frame(db.query("""
    SELECT project_name, AVG(avg_close_time_days) as avg_close, MIN(avg_close_time_days) as min_close
    FROM jira__project_enhanced
    GROUP BY project_name
"""))
combined = proj_data.merge(proj_enhanced, on='project_name')

# Get team data for the projects that have it
team_data = db.frame(db.query("""
    SELECT project_name, 
        COUNT(*) as team_size,
        SUM(at_churn_risk) as churn_risk,
        AVG(consistency_percentage) as avg_consistency,
        AVG(avg_sprint_completion_rate) as avg_sprint_completion,
        AVG(days_since_first_issue) as avg_tenure,
        AVG(estimate_accuracy_percentage) as avg_estimate_accuracy,
        AVG(overall_performance_score) as avg_performance
    FROM jira__team_performance_dashboard
    GROUP BY project_name
"""))
combined2 = combined.merge(team_data, on='project_name', how='left')

# Mark fast projects
combined2['is_fast'] = combined2['min_close'] < 15

# Create a comprehensive comparison chart
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. Regression ratio comparison
ax = axes[0, 0]
fast_data = combined2[combined2['is_fast']]
slow_data = combined2[~combined2['is_fast']]
ax.bar(['Fast Projects\n(<15d avg_close)', 'Other Projects\n(>=15d)'], 
       [fast_data['avg_regression'].mean(), slow_data['avg_regression'].mean()],
       yerr=[fast_data['avg_regression'].std(), slow_data['avg_regression'].std()],
       capsize=10, color=['coral', 'steelblue'], alpha=0.7)
ax.set_ylabel('Average Regression Ratio')
ax.set_title('Regression Ratio: Fast vs Other Projects\n(p < 0.001, significant)')

# 2. Lifecycle quality
ax = axes[0, 1]
ax.bar(['Fast Projects', 'Other Projects'], 
       [fast_data['avg_lqs'].mean(), slow_data['avg_lqs'].mean()],
       yerr=[fast_data['avg_lqs'].std(), slow_data['avg_lqs'].std()],
       capsize=10, color=['coral', 'steelblue'], alpha=0.7)
ax.set_ylabel('Avg Lifecycle Quality Score')
ax.set_title('Lifecycle Quality: Fast vs Other Projects\n(p < 0.001, significant)')

# 3. Bug rate
ax = axes[0, 2]
ax.bar(['Fast Projects', 'Other Projects'], 
       [fast_data['bug_rate'].mean(), slow_data['bug_rate'].mean()],
       yerr=[fast_data['bug_rate'].std(), slow_data['bug_rate'].std()],
       capsize=10, color=['coral', 'steelblue'], alpha=0.7)
ax.set_ylabel('Bug Rate')
ax.set_title('Bug Rate: Fast vs Other Projects\n(p = 0.52, not significant)')

# 4. Unusually fast rate
ax = axes[1, 0]
ax.bar(['Fast Projects', 'Other Projects'], 
       [fast_data['unusually_fast_rate'].mean(), slow_data['unusually_fast_rate'].mean()],
       yerr=[fast_data['unusually_fast_rate'].std(), slow_data['unusually_fast_rate'].std()],
       capsize=10, color=['coral', 'steelblue'], alpha=0.7)
ax.set_ylabel('Unusually Fast Rate')
ax.set_title('Unusually Fast Issues: Fast vs Other')

# 5. Blocked rate
ax = axes[1, 1]
ax.bar(['Fast Projects', 'Other Projects'], 
       [fast_data['blocked_rate'].mean(), slow_data['blocked_rate'].mean()],
       yerr=[fast_data['blocked_rate'].std(), slow_data['blocked_rate'].std()],
       capsize=10, color=['coral', 'steelblue'], alpha=0.7)
ax.set_ylabel('Blocked Issue Rate')
ax.set_title('Blocked Rate: Fast vs Other')

# 6. Deviation ratio
ax = axes[1, 2]
ax.bar(['Fast Projects', 'Other Projects'], 
       [fast_data['avg_deviation'].mean(), slow_data['avg_deviation'].mean()],
       yerr=[fast_data['avg_deviation'].std(), slow_data['avg_deviation'].std()],
       capsize=10, color=['coral', 'steelblue'], alpha=0.7)
ax.set_ylabel('Avg Lifecycle Deviation Ratio')
ax.set_title('Deviation: Fast vs Other')

plt.tight_layout()
plt.savefig('/work/fast_vs_other_detailed.png', dpi=150)
plt.close()

# Team stability chart
fig, ax = plt.subplots(figsize=(10, 6))
team_plot = combined2.dropna(subset=['team_size']).copy()
team_plot['stability_simple'] = 100 * (1 - team_plot['churn_risk'] / team_plot['team_size'])
team_plot['stability_weighted'] = team_plot['stability_simple'] * (team_plot['avg_consistency'] / 100)
team_plot['stability_combined'] = team_plot['stability_weighted'] * (team_plot['avg_sprint_completion'] * 100 / 100)

x = np.arange(len(team_plot))
width = 0.25
colors = ['coral' if f else 'steelblue' for f in team_plot['is_fast']]

ax.bar(x - width, team_plot['stability_simple'], width, label='Simple Stability (100% - churn%)', color='lightcoral', alpha=0.8)
ax.bar(x, team_plot['stability_weighted'], width, label='Weighted Stability (×consistency)', color='coral', alpha=0.8)
ax.bar(x + width, team_plot['stability_combined'], width, label='Combined (×sprint completion)', color='darkred', alpha=0.8)

ax.set_xticks(x)
ax.set_xticklabels([f"{p}\nclose={c:.0f}d" for p, c in zip(team_plot['project_name'], team_plot['avg_close'])], rotation=20)
ax.set_ylabel('Stability Score (%)')
ax.set_title('Team Stability Metrics by Project (Redefined)')
ax.legend()
plt.tight_layout()
plt.savefig('/work/team_stability_detailed.png', dpi=150)
plt.close()

print("\n\n=== Detailed stats for fast projects ===")
for _, row in fast_data.iterrows():
    print(f"\n{row['project_name']}:")
    print(f"  avg_close_time: {row['avg_close']:.1f}d (min: {row['min_close']:.0f}d)")
    print(f"  Bug rate: {row['bug_rate']:.4f}")
    print(f"  Avg regression ratio: {row['avg_regression']:.4f}")
    print(f"  Avg lifecycle quality: {row['avg_lqs']:.4f}")
    print(f"  Unusually fast rate: {row['unusually_fast_rate']:.4f}")
    print(f"  Blocked rate: {row['blocked_rate']:.4f}")
    print(f"  Avg risk score: {row['avg_risk']:.2f}")
    if pd.notna(row['team_size']):
        stability = 100 * (1 - row['churn_risk'] / row['team_size'])
        print(f"  Team size: {row['team_size']:.0f}, Churn risk: {row['churn_risk']:.0f}")
        print(f"  Team stability (simple): {stability:.1f}%")
        print(f"  Avg consistency: {row['avg_consistency']:.1f}%")

print("\n\n=== Statistical tests summary ===")
metrics = ['avg_regression', 'avg_lqs', 'bug_rate', 'unusually_fast_rate', 'stat_outlier_rate', 
           'above_normal_rate', 'blocked_rate', 'avg_risk', 'avg_intel', 'avg_cp', 'avg_deviation']
for m in metrics:
    fast_vals = fast_data[m].dropna()
    slow_vals = slow_data[m].dropna()
    if len(fast_vals) > 0 and len(slow_vals) > 0:
        t, p = stats.ttest_ind(fast_vals, slow_vals)
        print(f"  {m}: fast_mean={fast_vals.mean():.4f}, slow_mean={slow_vals.mean():.4f}, t={t:.3f}, p={p:.4f}")

print("\n\nAll figures saved.")