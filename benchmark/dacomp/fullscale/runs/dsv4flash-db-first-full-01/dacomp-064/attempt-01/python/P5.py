import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

# Get weekly issue counts from daily history for target stakeholders
weekly = db.frame(db.query("""
SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status
ORDER BY d.date_week
"""))
weekly['date_week'] = pd.to_datetime(weekly['date_week'])

# Pivot for status types
pivot = weekly.pivot_table(index='date_week', columns='status', values='n_issues', aggfunc='sum', fill_value=0)
pivot['total'] = pivot.sum(axis=1)
print("=== Weekly activity from daily history (target) ===")
# First 5 and last 5 weeks
print(pivot.head(5))
print("...")
print(pivot.tail(5))

# Plot weekly trend
plt.figure(figsize=(12,5))
plt.plot(pivot.index, pivot['total'], 'o-', label='Total Active Issues', color='navy', linewidth=2)
if 'In Progress' in pivot.columns:
    plt.plot(pivot.index, pivot['In Progress'], 's--', label='In Progress', color='orange', linewidth=2)
if 'Done' in pivot.columns:
    plt.plot(pivot.index, pivot['Done'], '^--', label='Done', color='green', linewidth=2)
plt.xlabel('Week', fontsize=11)
plt.ylabel('Issue Count', fontsize=11)
plt.title('Weekly Issue Activity (Target Stakeholders)', fontsize=13)
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('/work/weekly_activity.png', dpi=150)
plt.close()

# ============ Strategic Value vs Contribution Gap ============
prof = db.frame(db.query("""
SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
"""))
prof['influence_imbalance'] = prof['total_outbound_influence'] - prof['total_inbound_influence']
prof['assign_report_ratio'] = prof['issues_assigned'] / prof['issues_reported'].replace(0, np.nan)

# Strategic value gap: high strategic but low contribution
# Define "contribution" as a composite of issues_assigned, comments, and quality
prof['contribution_composite'] = (
    (prof['issues_assigned'] - prof['issues_assigned'].min()) / (prof['issues_assigned'].max() - prof['issues_assigned'].min()) +
    (prof['total_comments_authored'] - prof['total_comments_authored'].min()) / (prof['total_comments_authored'].max() - prof['total_comments_authored'].min()) +
    (prof['engagement_quality_score'] - prof['engagement_quality_score'].min()) / (prof['engagement_quality_score'].max() - prof['engagement_quality_score'].min())
) / 3

# Identify misalignment: high strategic value (>80) but low contribution (<median)
median_contrib = prof['contribution_composite'].median()
prof['strat_contrib_gap'] = prof['strategic_value_score'] - prof['contribution_composite'].rank(pct=True)*100

print("\n=== Strategic Value vs Contribution Gap Analysis ===")
high_strat_low_contrib = prof[(prof['strategic_value_score'] >= 80) & (prof['contribution_composite'] < median_contrib)]
low_strat_high_contrib = prof[(prof['strategic_value_score'] < 80) & (prof['contribution_composite'] >= median_contrib)]
print(f"High strategic (>80) but low contribution (<median): {len(high_strat_low_contrib)} ({len(high_strat_low_contrib)/len(prof)*100:.1f}%)")
print(f"Low strategic (<80) but high contribution (>=median): {len(low_strat_high_contrib)} ({len(low_strat_high_contrib)/len(prof)*100:.1f}%)")
print(f"These misaligned stakeholders have avg depth: {high_strat_low_contrib['engagement_depth_score'].mean():.2f} (vs overall {prof['engagement_depth_score'].mean():.2f})")
print(f"They have avg breadth: {high_strat_low_contrib['engagement_breadth_score'].mean():.2f} (vs overall {prof['engagement_breadth_score'].mean():.2f})")
print(f"Influence imbalance: {high_strat_low_contrib['influence_imbalance'].mean():.2f} (vs overall {prof['influence_imbalance'].mean():.2f})")

# ============ Network connections vs depth ============
print("\n=== Network Connections vs Depth ===")
prof['conn_group'] = pd.cut(prof['direct_network_connections'], bins=[0,30,50,70,100], labels=['Low(0-30)','Med(30-50)','High(50-70)','Very High(70+)'])
conn_analysis = prof.groupby('conn_group', observed=True).agg(
    n=('engagement_depth_score','count'),
    avg_depth=('engagement_depth_score','mean'),
    avg_breadth=('engagement_breadth_score','mean'),
    avg_imbalance=('influence_imbalance','mean'),
    at_risk_share=('engagement_risk_status', lambda x: (x.isin(['At Risk','Disengaged'])).mean())
).round(2)
print(conn_analysis)

# ============ Response pattern vs depth ============
print("\n=== Response Pattern Analysis ===")
rp_analysis = prof.groupby('response_pattern_type').agg(
    n=('engagement_depth_score','count'),
    avg_depth=('engagement_depth_score','mean'),
    avg_breadth=('engagement_breadth_score','mean'),
    avg_imbalance=('influence_imbalance','mean'),
    at_risk_share=('engagement_risk_status', lambda x: (x.isin(['At Risk','Disengaged'])).mean())
).round(2).sort_values('avg_depth')
print(rp_analysis)