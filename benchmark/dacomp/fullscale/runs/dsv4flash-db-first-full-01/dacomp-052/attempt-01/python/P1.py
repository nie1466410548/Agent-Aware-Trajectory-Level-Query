import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Fetch target team data
result = db.query("""
SELECT team_name, team_size_category, workload_balance_status, team_maturity_level,
  total_projects, enterprise_projects, large_projects, medium_projects, small_projects,
  avg_completion_rate, avg_project_health, avg_project_performance, avg_quality_rate,
  unique_team_members, avg_tasks_per_member, high_workload_members, high_risk_members,
  avg_estimated_completion_days, on_schedule_rate_pct, avg_risk_percentage,
  overdue_projects, overdue_team_tasks, total_team_tasks, completed_team_tasks,
  active_team_tasks, avg_project_velocity, avg_member_completion_rate,
  avg_tasks_per_assignee_across_projects, total_project_assignments,
  top_performers, high_performers, solid_performers, developing_performers, underperformers
FROM asana__team_efficiency_metrics
WHERE collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70
""")
df = db.frame(result)

# Compute derived columns
df['pct_large_enterprise'] = (df['enterprise_projects'] + df['large_projects']) * 100.0 / df['total_projects']
df['pct_high_workload'] = df['high_workload_members'] * 100.0 / df['unique_team_members']
df['pct_high_risk'] = df['high_risk_members'] * 100.0 / df['unique_team_members']
df['pct_overdue_tasks'] = df['overdue_team_tasks'] * 100.0 / df['total_team_tasks']
df['pct_active_tasks'] = df['active_team_tasks'] * 100.0 / df['total_team_tasks']
df['pct_completed_tasks'] = df['completed_team_tasks'] * 100.0 / df['total_team_tasks']
df['tasks_per_member'] = df['total_team_tasks'] / df['unique_team_members']
df['performer_ratio'] = (df['top_performers'] + df['high_performers'] + df['solid_performers']) / (df['developing_performers'] + df['underperformers'] + 1)

# Print summary stats
print("=== Target Teams Summary ===")
print(f"Number of teams: {len(df)}")
print(f"\nAvg completion rate: {df['avg_completion_rate'].mean():.1f}% (range: {df['avg_completion_rate'].min():.1f}% - {df['avg_completion_rate'].max():.1f}%)")
print(f"Avg % large/enterprise projects: {df['pct_large_enterprise'].mean():.1f}%")
print(f"Avg estimated completion days: {df['avg_estimated_completion_days'].mean():.1f}")
print(f"Avg % high workload members: {df['pct_high_workload'].mean():.1f}%")
print(f"Avg on-schedule rate: {df['on_schedule_rate_pct'].mean():.1f}%")
print(f"Avg risk %: {df['avg_risk_percentage'].mean():.1f}%")

# Correlation analysis
features = ['pct_large_enterprise', 'avg_estimated_completion_days', 'pct_high_workload',
            'on_schedule_rate_pct', 'avg_risk_percentage', 'pct_overdue_tasks',
            'pct_high_risk', 'avg_tasks_per_member', 'avg_member_completion_rate',
            'unique_team_members', 'total_projects', 'avg_project_velocity']

corr = df[['avg_completion_rate'] + features].corr()['avg_completion_rate'].drop('avg_completion_rate')
print("\n=== Correlation with avg_completion_rate ===")
for feat in features:
    print(f"  {feat}: {corr[feat]:.3f}")

# ====== Figure 1: Scatter plots of key factors ======
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
ax = axes.flatten()

scatter_vars = [
    ('pct_large_enterprise', '% Large/Enterprise Projects', 'green'),
    ('avg_estimated_completion_days', 'Avg Estimated Completion (days)', 'blue'),
    ('pct_high_workload', '% High Workload Members', 'red'),
    ('on_schedule_rate_pct', 'On-Schedule Rate (%)', 'purple'),
    ('avg_risk_percentage', 'Avg Risk %', 'orange'),
    ('pct_overdue_tasks', '% Overdue Tasks', 'brown')
]

for i, (var, label, color) in enumerate(scatter_vars):
    ax[i].scatter(df[var], df['avg_completion_rate'], c=color, alpha=0.7, s=80, edgecolors='black', linewidth=0.5)
    # Fit a trend line
    z = np.polyfit(df[var], df['avg_completion_rate'], 1)
    p = np.poly1d(z)
    x_sorted = np.sort(df[var])
    ax[i].plot(x_sorted, p(x_sorted), 'k--', alpha=0.6, linewidth=1.5)
    ax[i].set_xlabel(label, fontsize=12)
    ax[i].set_ylabel('Avg Completion Rate (%)', fontsize=12)
    ax[i].grid(True, alpha=0.3)
    r2 = f"r={corr[var]:.2f}"
    ax[i].text(0.05, 0.95, r2, transform=ax[i].transAxes, fontsize=11, 
               verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))

plt.suptitle('Target Teams: Completion Rate vs. Key Factors', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('/work/target_teams_scatter.png', dpi=150, bbox_inches='tight')
plt.close()

# ====== Figure 2: Project size composition ======
fig, ax = plt.subplots(figsize=(12, 6))
# Average project composition
avg_ent = df['enterprise_projects'].mean()
avg_large = df['large_projects'].mean()
avg_med = df['medium_projects'].mean()
avg_small = df['small_projects'].mean()

categories = ['Enterprise', 'Large', 'Medium', 'Small']
values = [avg_ent, avg_large, avg_med, avg_small]
colors_bar = ['#2E86AB', '#A23B72', '#F18F01', '#C73E1D']

bars = ax.bar(categories, values, color=colors_bar, edgecolor='black', linewidth=0.8)
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.05, 
            f'{val:.1f}', ha='center', va='bottom', fontsize=12, fontweight='bold')

ax.set_ylabel('Average Number of Projects per Team', fontsize=13)
ax.set_title('Average Project Size Composition of Target Teams', fontsize=15)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/project_size_composition.png', dpi=150, bbox_inches='tight')
plt.close()

# ====== Figure 3: Workload distribution ======
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Workload balance status
wl_counts = df['workload_balance_status'].value_counts()
colors_wl = ['#E74C3C', '#F39C12', '#2ECC71']
axes[0].pie(wl_counts.values, labels=wl_counts.index, autopct='%1.1f%%', 
            colors=colors_wl, startangle=90, explode=[0.05]*3)
axes[0].set_title('Workload Balance Status', fontsize=14)

# Team size category
ts_counts = df['team_size_category'].value_counts()
colors_ts = ['#3498DB', '#9B59B6', '#1ABC9C']
axes[1].pie(ts_counts.values, labels=ts_counts.index, autopct='%1.1f%%',
            colors=colors_ts, startangle=90, explode=[0.05]*3)
axes[1].set_title('Team Size Category', fontsize=14)

plt.suptitle('Target Team Composition', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('/work/team_composition_pies.png', dpi=150, bbox_inches='tight')
plt.close()

# ====== Figure 4: Task status breakdown ======
fig, ax = plt.subplots(figsize=(10, 6))
task_status = ['Completed', 'Active', 'Overdue']
task_pcts = [df['pct_completed_tasks'].mean(), df['pct_active_tasks'].mean(), df['pct_overdue_tasks'].mean()]
colors_task = ['#2ECC71', '#3498DB', '#E74C3C']
bars = ax.bar(task_status, task_pcts, color=colors_task, edgecolor='black', linewidth=0.8, width=0.5)
for bar, val in zip(bars, task_pcts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
            f'{val:.1f}%', ha='center', va='bottom', fontsize=13, fontweight='bold')
ax.set_ylabel('Percentage of Total Tasks', fontsize=13)
ax.set_title('Average Task Status Distribution Among Target Teams', fontsize=15)
ax.set_ylim(0, 70)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/task_status_breakdown.png', dpi=150, bbox_inches='tight')
plt.close()

print("\nFigures saved successfully.")