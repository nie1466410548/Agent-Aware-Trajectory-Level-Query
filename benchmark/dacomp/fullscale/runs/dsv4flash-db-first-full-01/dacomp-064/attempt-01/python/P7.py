
import pandas as pd, numpy as np, matplotlib.pyplot as plt

prof = db.frame(db.query("""
SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
"""))
prof['influence_imbalance'] = prof['total_outbound_influence'] - prof['total_inbound_influence']
prof['influence_ratio'] = prof['total_outbound_influence'] / prof['total_inbound_influence'].replace(0, 1)
prof['ar_ratio'] = prof['issues_assigned'] / prof['issues_reported'].replace(0, np.nan)
prof['contrib_rank'] = ((
    (prof['issues_assigned'] - prof['issues_assigned'].min()) / (prof['issues_assigned'].max() - prof['issues_assigned'].min()) +
    (prof['total_comments_authored'] - prof['total_comments_authored'].min()) / (prof['total_comments_authored'].max() - prof['total_comments_authored'].min()) +
    (prof['engagement_quality_score'] - prof['engagement_quality_score'].min()) / (prof['engagement_quality_score'].max() - prof['engagement_quality_score'].min())
) / 3).rank(pct=True)

# close time data
cat_close = db.frame(db.query("""
SELECT p.project_category_id, 
  (julianday(i.resolved_at)-julianday(i.created_at)) AS close_days,
  strftime('%Y-%m', i.resolved_at) AS month
FROM jira__issue_enhanced i
JOIN jira__stakeholder_engagement_insights s ON i.assignee_user_id = s.stakeholder_id
JOIN jira__project_enhanced p ON i.project_id = p.project_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
  AND i.resolved_at IS NOT NULL AND i.resolved_at < '2025-11-01'
"""))
close_trend = cat_close.groupby('month').agg(avg_close=('close_days','mean')).reset_index()

# weekly pivot
weekly_status = db.frame(db.query("""
SELECT d.date_week, d.status, COUNT(DISTINCT d.issue_id) AS n_issues
FROM jira__daily_issue_field_history d
JOIN jira__stakeholder_engagement_insights s ON d.assignee = s.stakeholder_id
WHERE s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3
GROUP BY d.date_week, d.status ORDER BY d.date_week
"""))
weekly_status['date_week'] = pd.to_datetime(weekly_status['date_week'])
pivot = weekly_status.pivot_table(index='date_week', columns='status', values='n_issues', aggfunc='sum', fill_value=0)

fig, axes = plt.subplots(2, 3, figsize=(16, 10))

ax = axes[0,0]
sc = ax.scatter(prof['engagement_breadth_score'], prof['engagement_depth_score'],
                c=prof['influence_imbalance'], cmap='coolwarm', alpha=0.6, s=20)
ax.set_xlabel('Engagement Breadth'); ax.set_ylabel('Engagement Depth')
ax.set_title('Depth vs Breadth (color = influence imbalance)')
plt.colorbar(sc, ax=ax, label='Influence Imbalance')

ax = axes[0,1]
ax.scatter(prof['engagement_breadth_score'], prof['ar_ratio'], alpha=0.5, s=20, c='green')
ax.set_xlabel('Engagement Breadth'); ax.set_ylabel('Assign/Report Ratio')
ax.set_title('Problem-Solving Efficiency vs Breadth')

ax = axes[0,2]
ax.scatter(prof['strategic_value_score'], prof['contrib_rank'], alpha=0.5, s=20, c='purple')
ax.axhline(0.5, color='gray', linestyle='--', alpha=0.5); ax.axvline(80, color='gray', linestyle='--', alpha=0.5)
ax.set_xlabel('Strategic Value Score'); ax.set_ylabel('Contribution Percentile')
ax.set_title('Strategic Value vs Actual Contribution')

ax = axes[1,0]
ax.plot(close_trend['month'], close_trend['avg_close'], 'o-', color='red', linewidth=2)
ax.set_xlabel('Month'); ax.set_ylabel('Avg Close Time (days)')
ax.set_title('Close Time Trend (Target)')
ax.tick_params(axis='x', rotation=45)

ax = axes[1,1]
ps = pivot.tail(10)
ax.plot(ps.index, ps['Testing'], 'o-', label='Testing', color='orange', linewidth=2)
ax.plot(ps.index, ps['Done'], 's--', label='Done', color='green', linewidth=2)
ax.set_xlabel('Week'); ax.set_ylabel('Issue Count')
ax.set_title('Testing Backlog vs Completion (Target)')
ax.legend(); ax.tick_params(axis='x', rotation=45)

ax = axes[1,2]
ax.hist(prof['influence_imbalance'], bins=30, color='steelblue', edgecolor='black', alpha=0.7)
ax.axvline(prof['influence_imbalance'].mean(), color='red', linestyle='--', label=f"Mean: {prof['influence_imbalance'].mean():.1f}")
ax.set_xlabel('Influence Imbalance (Outbound - Inbound)'); ax.set_ylabel('Count')
ax.set_title('Influence Imbalance Distribution')
ax.legend()

plt.tight_layout()
plt.savefig('/work/final_analysis.png', dpi=150)
plt.close()

print("Figure saved. Key stats:")
print(f"Extreme Outbound (>2x): {(prof['influence_ratio']>2).sum()} of {len(prof)}")
print(f"Mean influence imbalance: {prof['influence_imbalance'].mean():.2f}")
print(f"Close time Apr->Oct: {close_trend[close_trend['month']=='2025-04']['avg_close'].values[0]:.2f} -> {close_trend[close_trend['month']=='2025-10']['avg_close'].values[0]:.2f} days")
