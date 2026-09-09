import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

# Monthly close times for target stakeholders
target_close = db.frame(db.query("""
SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.work_ratio,
  i.issue_type
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL
"""))
target_close['month'] = pd.to_datetime(target_close['month'] + '-01')
target_close = target_close[target_close['month'] < '2025-11-01']  # exclude partial Nov

# Non-target monthly close times
other_close = db.frame(db.query("""
SELECT 
  strftime('%Y-%m', i.resolved_at) AS month,
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.work_ratio
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
WHERE NOT (s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3)
  AND i.resolved_at IS NOT NULL
"""))
other_close['month'] = pd.to_datetime(other_close['month'] + '-01')
other_close = other_close[other_close['month'] < '2025-11-01']

# Monthly stats
target_monthly = target_close.groupby('month').agg(
    n_issues=('close_days','count'),
    avg_close_days=('close_days','mean'),
    median_close_days=('close_days','median'),
    avg_work_ratio=('work_ratio','mean')
).round(2)
other_monthly = other_close.groupby('month').agg(
    n_issues=('close_days','count'),
    avg_close_days=('close_days','mean'),
    median_close_days=('close_days','median'),
    avg_work_ratio=('work_ratio','mean')
).round(2)

print("=== Target Group Monthly Close Time Trend ===")
print(target_monthly)
print("\n=== Non-Target Group Monthly Close Time Trend ===")
print(other_monthly)

# Plot
fig, axes = plt.subplots(1, 2, figsize=(14,5))

ax1 = axes[0]
ax1.plot(target_monthly.index, target_monthly['avg_close_days'], 'o-', label='Target (High Impact)', color='red', linewidth=2)
ax1.plot(other_monthly.index, other_monthly['avg_close_days'], 's--', label='Non-Target', color='blue', linewidth=2)
ax1.set_xlabel('Month', fontsize=11)
ax1.set_ylabel('Avg Close Time (days)', fontsize=11)
ax1.set_title('Problem-Solving Efficiency: Close Time Trend', fontsize=12)
ax1.legend()
ax1.grid(alpha=0.3)

ax2 = axes[1]
ax2.bar(target_monthly.index - pd.Timedelta(days=7), target_monthly['n_issues'], width=12, label='Target (High Impact)', color='red', alpha=0.7)
ax2.bar(other_monthly.index + pd.Timedelta(days=7), other_monthly['n_issues'], width=12, label='Non-Target', color='blue', alpha=0.7)
ax2.set_xlabel('Month', fontsize=11)
ax2.set_ylabel('Issues Resolved', fontsize=11)
ax2.set_title('Resolution Volume Trend', fontsize=12)
ax2.legend()
ax2.grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/work/monthly_trends.png', dpi=150)
plt.close()

# By issue type, analyze close time trend for target
type_trend = target_close.groupby(['month','issue_type']).agg(
    avg_close=('close_days','mean'),
    n=('close_days','count')
).round(2).reset_index()
pivot = type_trend.pivot_table(index='month', columns='issue_type', values='avg_close')
print("\n=== Close time by issue type (target group) ===")
print(pivot.round(2))