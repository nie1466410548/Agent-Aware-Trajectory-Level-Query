import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

# ============ Testing bottleneck analysis ============
weekly_status = db.frame(db.query("""
SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status
ORDER BY d.date_week
"""))
weekly_status['date_week'] = pd.to_datetime(weekly_status['date_week'])
pivot = weekly_status.pivot_table(index='date_week', columns='status', values='n_issues', aggfunc='sum', fill_value=0)

# Compute testing ratio
pivot['testing_ratio'] = pivot['Testing'] / (pivot['Done'] + pivot['Testing']).replace(0, 1)
print("=== Testing Bottleneck Analysis ===")
print(pivot[['Testing','Done','testing_ratio']].tail(10))

# ============ Influence propagation analysis ============
prof = db.frame(db.query("""
SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
"""))
prof['influence_imbalance'] = prof['total_outbound_influence'] - prof['total_inbound_influence']
prof['influence_ratio'] = prof['total_outbound_influence'] / prof['total_inbound_influence'].replace(0, 1)

# Categorize influence propagation patterns
prof['influence_type'] = 'Balanced'
prof.loc[(prof['influence_ratio'] > 1.5) & (prof['total_outbound_influence'] > prof['total_outbound_influence'].median()), 'influence_type'] = 'High Outbound Hub'
prof.loc[(prof['influence_ratio'] < 0.67) & (prof['total_inbound_influence'] > prof['total_inbound_influence'].median()), 'influence_type'] = 'High Inbound Hub'
prof.loc[(prof['influence_ratio'] > 2.0), 'influence_type'] = 'Extreme Outbound'
prof.loc[(prof['influence_ratio'] < 0.5), 'influence_type'] = 'Extreme Inbound'

print("\n=== Influence Propagation Patterns ===")
print(prof['influence_type'].value_counts())

# Compare depth by influence type
inf_analysis = prof.groupby('influence_type').agg(
    n=('engagement_depth_score','count'),
    avg_depth=('engagement_depth_score','mean'),
    avg_breadth=('engagement_breadth_score','mean'),
    avg_imbalance=('influence_imbalance','mean'),
    avg_connections=('direct_network_connections','mean'),
    at_risk_share=('engagement_risk_status', lambda x: (x.isin(['At Risk','Disengaged'])).mean())
).round(2)
print(inf_analysis)

# ============ Project type / category impact on close time ============
# Get project category for each issue resolved by target
cat_close = db.frame(db.query("""
SELECT p.project_category_id, 
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  i.issue_type, strftime('%Y-%m', i.resolved_at) AS month
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL
  AND i.resolved_at < '2025-11-01'
"""))

cat_monthly = cat_close.groupby(['project_category_id','month']).agg(
    avg_close=('close_days','mean'),
    n=('close_days','count')
).round(2).reset_index()

print("\n=== Close Time by Project Category (Target) ===")
print(cat_close.groupby('project_category_id').agg(
    avg_close=('close_days','mean'),
    median_close=('close_days','median'),
    n=('close_days','count')
).round(2).sort_values('avg_close'))

# ============ Final visualization: Influence vs Depth scatter ============
fig, axes = plt.subplots(2, 3, figsize=(16, 10))

# 1. Depth vs Breadth
ax = axes[0,0]
scatter = ax.scatter(prof['engagement_breadth_score'], prof['engagement_depth_score'], 
                     c=prof['influence_imbalance'], cmap='coolwarm', alpha=0.6, s=20)
ax.set_xlabel('Engagement Breadth'); ax.set_ylabel('Engagement Depth')
ax.set_title('Depth vs Breadth (color=influence imbalance)')
plt.colorbar(scatter, ax=ax, label='Influence Imbalance')

# 2. Assign/Report Ratio vs Breadth
ax = axes[0,1]
prof['ar_ratio'] = prof['issues_assigned'] / prof['issues_reported'].replace(0, np.nan)
ax.scatter(prof['engagement_breadth_score'], prof['ar_ratio'], alpha=0.5, s=20, c='green')
ax.set_xlabel('Engagement Breadth'); ax.set_ylabel('Assign/Report Ratio')
ax.set_title('Problem-Solving Efficiency vs Breadth')

# 3. Strategic value vs Contribution composite
ax = axes[0,2]
prof['contrib_rank'] = prof['contribution_composite'].rank(pct=True)
ax.scatter(prof['strategic_value_score'], prof['contrib_rank'], alpha=0.5, s=20, c='purple')
ax.axhline(0.5, color='gray', linestyle='--', alpha=0.5)
ax.axvline(80, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Strategic Value Score'); ax.set_ylabel('Contribution Percentile')
ax.set_title('Strategic Value vs Actual Contribution')

# 4. Close time trend by month
ax = axes[1,0]
close_trend = cat_close.groupby('month').agg(avg_close=('close_days','mean')).reset_index()
ax.plot(close_trend['month'], close_trend['avg_close'], 'o-', color='red', linewidth=2)
ax.set_xlabel('Month'); ax.set_ylabel('Avg Close Time (days)')
ax.set_title('Close Time Trend (Target)')
ax.tick_params(axis='x', rotation=45)

# 5. Testing bottleneck
ax = axes[1,1]
pivot_slice = pivot.tail(10)
ax.plot(pivot_slice.index, pivot_slice['Testing'], 'o-', label='Testing', color='orange', linewidth=2)
ax.plot(pivot_slice.index, pivot_slice['Done'], 's--', label='Done', color='green', linewidth=2)
ax.set_xlabel('Week'); ax.set_ylabel('Issue Count')
ax.set_title('Testing Bottleneck in Recent Weeks')
ax.legend()
ax.tick_params(axis='x', rotation=45)

# 6. Influence imbalance histogram
ax = axes[1,2]
ax.hist(prof['influence_imbalance'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
ax.axvline(prof['influence_imbalance'].mean(), color='red', linestyle='--', label=f"Mean: {prof['influence_imbalance'].mean():.1f}")
ax.set_xlabel('Influence Imbalance (Outbound - Inbound)')
ax.set_ylabel('Count')
ax.set_title('Influence Imbalance Distribution')
ax.legend()

plt.tight_layout()
plt.savefig('/work/final_analysis.png', dpi=150)
plt.close()

print("\n=== Summary Statistics ===")
print(f"Target cohort size: {len(prof)}")
print(f"Avg depth: {prof['engagement_depth_score'].mean():.2f}")
print(f"Avg breadth: {prof['engagement_breadth_score'].mean():.2f}")
print(f"Avg influence imbalance: {prof['influence_imbalance'].mean():.2f}")
print(f"Avg strategic value: {prof['strategic_value_score'].mean():.2f}")
print(f"At-risk share: {(prof['engagement_risk_status'].isin(['At Risk','Disengaged'])).mean()*100:.1f}%")
print(f"Extreme outbound influence (>2x ratio): {(prof['influence_ratio']>2).sum()} stakeholders")