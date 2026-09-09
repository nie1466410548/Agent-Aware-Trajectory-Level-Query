import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Get comparison data
result = db.query("""
SELECT *, 
  CASE WHEN collaboration_efficiency_score >= 8 AND resource_optimization_score >= 8 AND avg_completion_rate < 70 THEN 'target' ELSE 'other' END AS grp
FROM asana__team_efficiency_metrics
""")
df = db.frame(result)

# Derived columns
df['pct_large_enterprise'] = (df['enterprise_projects'] + df['large_projects']) * 100.0 / df['total_projects']
df['pct_high_workload'] = df['high_workload_members'] * 100.0 / df['unique_team_members']
df['pct_overdue_tasks'] = df['overdue_team_tasks'] * 100.0 / df['total_team_tasks']
df['pct_active_tasks'] = df['active_team_tasks'] * 100.0 / df['total_team_tasks']
df['pct_completed_tasks'] = df['completed_team_tasks'] * 100.0 / df['total_team_tasks']

# ====== Figure 1: Rank comparison ======
fig, ax = plt.subplots(figsize=(10, 6))
target = df[df['grp'] == 'target']
other = df[df['grp'] == 'other']

rank_cols = ['efficiency_rank', 'performance_rank', 'schedule_reliability_rank', 'quality_rank']
rank_labels = ['Efficiency\nRank', 'Performance\nRank', 'Schedule\nReliability Rank', 'Quality\nRank']
target_means = [target[c].mean() for c in rank_cols]
other_means = [other[c].mean() for c in rank_cols]

x = np.arange(len(rank_labels))
width = 0.35
bars1 = ax.bar(x - width/2, target_means, width, label='Target Teams (n=37)', color='#E74C3C', edgecolor='black')
bars2 = ax.bar(x + width/2, other_means, width, label='Other Teams (n=13)', color='#3498DB', edgecolor='black')

for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2, h + 0.5, f'{h:.1f}', ha='center', va='bottom', fontsize=10)

ax.set_ylabel('Average Rank (lower is better)', fontsize=13)
ax.set_title('Team Rank Comparison: Target vs Other Teams', fontsize=15)
ax.set_xticks(x)
ax.set_xticklabels(rank_labels, fontsize=11)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/rank_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# ====== Figure 2: Project size comparison ======
fig, ax = plt.subplots(figsize=(10, 6))
size_cols = ['enterprise_projects', 'large_projects', 'medium_projects', 'small_projects']
size_labels = ['Enterprise', 'Large', 'Medium', 'Small']
target_means = [target[c].mean() for c in size_cols]
other_means = [other[c].mean() for c in size_cols]

x = np.arange(len(size_labels))
bars1 = ax.bar(x - width/2, target_means, width, label='Target Teams (n=37)', color='#E74C3C', edgecolor='black')
bars2 = ax.bar(x + width/2, other_means, width, label='Other Teams (n=13)', color='#3498DB', edgecolor='black')

for bars in [bars1, bars2]:
    for bar in bars:
        h = bar.get_height()
        if h > 0.1:
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.05, f'{h:.2f}', ha='center', va='bottom', fontsize=10)

ax.set_ylabel('Average Number of Projects', fontsize=13)
ax.set_title('Project Size Distribution Comparison', fontsize=15)
ax.set_xticks(x)
ax.set_xticklabels(size_labels, fontsize=11)
ax.legend(fontsize=11)
ax.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('/work/project_size_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# ====== Figure 3: Metrics radar chart ======
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

metrics = ['avg_completion_rate', 'avg_quality_rate', 'on_schedule_rate_pct', 
           'avg_project_health', 'avg_project_performance', 'avg_risk_percentage']
metric_labels = ['Completion\nRate', 'Quality\nRate', 'On-Schedule\nRate', 
                 'Project\nHealth', 'Project\nPerformance', 'Risk\n%']

# Normalize for radar
target_vals = [target[m].mean() for m in metrics]
other_vals = [other[m].mean() for m in metrics]

# For risk percentage, lower is better, so invert
# Normalize all to 0-100 scale
all_vals = target_vals + other_vals
max_vals = {}
for m in metrics:
    max_vals[m] = max(df[m].max(), 1)  # avoid division by zero

target_norm = [target[m].mean() / max_vals[m] * 100 for m in metrics]
other_norm = [other[m].mean() / max_vals[m] * 100 for m in metrics]

angles = np.linspace(0, 2 * np.pi, len(metrics), endpoint=False).tolist()
angles += angles[:1]

target_norm += target_norm[:1]
other_norm += other_norm[:1]

ax.plot(angles, target_norm, 'o-', linewidth=2, label='Target Teams', color='#E74C3C')
ax.fill(angles, target_norm, alpha=0.1, color='#E74C3C')
ax.plot(angles, other_norm, 'o-', linewidth=2, label='Other Teams', color='#3498DB')
ax.fill(angles, other_norm, alpha=0.1, color='#3498DB')

ax.set_xticks(angles[:-1])
ax.set_xticklabels(metric_labels, fontsize=10)
ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1), fontsize=12)
ax.set_title('Performance Metrics Comparison (Normalized)', fontsize=15, pad=20)
plt.tight_layout()
plt.savefig('/work/radar_comparison.png', dpi=150, bbox_inches='tight')
plt.close()

# ====== Figure 4: Workload and task scatter ======
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Scatter: Tasks per member vs completion rate
for grp_name, color, marker in [('target', '#E74C3C', 'o'), ('other', '#3498DB', 's')]:
    sub = df[df['grp'] == grp_name]
    axes[0].scatter(sub['avg_tasks_per_member'], sub['avg_completion_rate'], 
                    c=color, marker=marker, s=80, alpha=0.7, edgecolors='black', linewidth=0.5, label=grp_name)
axes[0].set_xlabel('Avg Tasks Per Member', fontsize=12)
axes[0].set_ylabel('Avg Completion Rate (%)', fontsize=12)
axes[0].set_title('Workload Intensity vs Completion', fontsize=13)
axes[0].legend(fontsize=11)
axes[0].grid(True, alpha=0.3)

# Scatter: Estimated days vs completion rate
for grp_name, color, marker in [('target', '#E74C3C', 'o'), ('other', '#3498DB', 's')]:
    sub = df[df['grp'] == grp_name]
    axes[1].scatter(sub['avg_estimated_completion_days'], sub['avg_completion_rate'], 
                    c=color, marker=marker, s=80, alpha=0.7, edgecolors='black', linewidth=0.5, label=grp_name)
axes[1].set_xlabel('Avg Estimated Completion Days', fontsize=12)
axes[1].set_ylabel('Avg Completion Rate (%)', fontsize=12)
axes[1].set_title('Project Complexity vs Completion', fontsize=13)
axes[1].legend(fontsize=11)
axes[1].grid(True, alpha=0.3)

plt.suptitle('Workload & Complexity Drivers', fontsize=15, y=1.02)
plt.tight_layout()
plt.savefig('/work/workload_complexity_scatter.png', dpi=150, bbox_inches='tight')
plt.close()

print("All comparison figures saved.")
print(f"\n=== Key Summary Stats ===")
print(f"Target teams (n={len(target)}):")
print(f"  Avg completion rate: {target['avg_completion_rate'].mean():.1f}%")
print(f"  Avg quality rate: {target['avg_quality_rate'].mean():.1f}%")
print(f"  Avg on-schedule rate: {target['on_schedule_rate_pct'].mean():.1f}%")
print(f"  Avg % large/enterprise: {target['pct_large_enterprise'].mean():.1f}%")
print(f"  Avg estimated days: {target['avg_estimated_completion_days'].mean():.1f}")
print(f"  Avg high workload %: {target['pct_high_workload'].mean():.1f}%")
print(f"  Avg schedule reliability rank: {target['schedule_reliability_rank'].mean():.1f}")
print(f"  Avg efficiency rank: {target['efficiency_rank'].mean():.1f}")
print(f"  Avg quality rank: {target['quality_rank'].mean():.1f}")
print(f"\nOther teams (n={len(other)}):")
print(f"  Avg completion rate: {other['avg_completion_rate'].mean():.1f}%")
print(f"  Avg quality rate: {other['avg_quality_rate'].mean():.1f}%")
print(f"  Avg on-schedule rate: {other['on_schedule_rate_pct'].mean():.1f}%")
print(f"  Avg % large/enterprise: {other['pct_large_enterprise'].mean():.1f}%")
print(f"  Avg estimated days: {other['avg_estimated_completion_days'].mean():.1f}")
print(f"  Avg high workload %: {other['pct_high_workload'].mean():.1f}%")
print(f"  Avg schedule reliability rank: {other['schedule_reliability_rank'].mean():.1f}")
print(f"  Avg efficiency rank: {other['efficiency_rank'].mean():.1f}")
print(f"  Avg quality rank: {other['quality_rank'].mean():.1f}")