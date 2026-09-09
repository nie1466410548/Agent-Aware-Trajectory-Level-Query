import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Workload of churn-risk members in fast project teams
print("=== Data Analytics Delta: Workload of at-risk members ===")
dad_members = db.frame(db.query("""
    SELECT user_display_name, total_assigned_issues, resolved_issues, at_churn_risk,
           consistency_percentage, avg_resolution_days, bug_issues, overall_performance_score,
           estimate_accuracy_percentage
    FROM jira__team_performance_dashboard
    WHERE project_name = 'Data Analytics Delta'
    ORDER BY at_churn_risk DESC
"""))
dad_members['at_risk_label'] = dad_members['at_churn_risk'].map({1: 'AT RISK', 0: 'stable'})
print(dad_members.to_string())
dad_at_risk_work = dad_members[dad_members['at_churn_risk']==1]['total_assigned_issues'].sum()
dad_total_work = dad_members['total_assigned_issues'].sum()
print(f"\nAt-risk members handle {dad_at_risk_work}/{dad_total_work} = {dad_at_risk_work/dad_total_work*100:.1f}% of assigned issues")

print("\n\n=== Mobile App Delta: Workload of at-risk members ===")
mad_members = db.frame(db.query("""
    SELECT user_display_name, total_assigned_issues, resolved_issues, at_churn_risk,
           consistency_percentage, avg_resolution_days, bug_issues, overall_performance_score,
           estimate_accuracy_percentage
    FROM jira__team_performance_dashboard
    WHERE project_name = 'Mobile App Delta'
    ORDER BY at_churn_risk DESC
"""))
mad_members['at_risk_label'] = mad_members['at_churn_risk'].map({1: 'AT RISK', 0: 'stable'})
print(mad_members.to_string())
mad_at_risk_work = mad_members[mad_members['at_churn_risk']==1]['total_assigned_issues'].sum()
mad_total_work = mad_members['total_assigned_issues'].sum()
print(f"\nAt-risk members handle {mad_at_risk_work}/{mad_total_work} = {mad_at_risk_work/mad_total_work*100:.1f}% of assigned issues")

# Compare with slow project teams
print("\n\n=== Comparison Teams ===")
for proj in ['API Gateway V3', 'Mobile App Gamma', 'User Management V3']:
    tm = db.frame(db.query(f"""
        SELECT total_assigned_issues, at_churn_risk
        FROM jira__team_performance_dashboard
        WHERE project_name = '{proj}'
    """))
    at_risk_work = tm[tm['at_churn_risk']==1]['total_assigned_issues'].sum()
    total_work = tm['total_assigned_issues'].sum()
    print(f"  {proj}: at-risk workload = {at_risk_work}/{total_work} ({at_risk_work/total_work*100:.1f}%), team_size={len(tm)}")

# Summary visualization of the key finding: speed vs stability vs quality
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Panel 1: Team stability vs speed
ax = axes[0]
projects = ['Data Analytics Delta', 'Mobile App Delta', 'Mobile App Gamma', 'API Gateway V3', 'User Management V3']
close_times = [13, 14, 19, 67, 51]
stabilities = [66.7, 80.0, 87.5, 90.0, 82.4]
colors = ['coral', 'coral', 'steelblue', 'steelblue', 'steelblue']
sc = ax.scatter(close_times, stabilities, c=colors, s=150, alpha=0.8)
for i, p in enumerate(projects):
    ax.annotate(p.replace(' Data Analytics', '\nData Analytics'), (close_times[i], stabilities[i]), 
                textcoords="offset points", xytext=(8, 5), fontsize=8)
ax.set_xlabel('Average Close Time (days)')
ax.set_ylabel('Team Stability % (100% - churn risk%)')
ax.set_title('Speed vs Team Stability\n(Fast projects show lowest stability)')
ax.axvline(x=15, color='red', linestyle='--', alpha=0.5, label='15-day threshold')
ax.legend()

# Panel 2: Regression ratio vs speed (all projects)
ax = axes[1]
combined = db.frame(db.query("""
    SELECT p.project_name, p.avg_close_time, i.avg_regression, i.avg_lqs
    FROM (SELECT project_name, AVG(avg_close_time_days) as avg_close_time FROM jira__project_enhanced GROUP BY project_name) p
    JOIN (SELECT project_name, AVG(regression_ratio) as avg_regression, AVG(lifecycle_quality_score) as avg_lqs FROM jira__issue_intelligence_analytics GROUP BY project_name) i
    ON p.project_name = i.project_name
"""))
ax.scatter(combined['avg_close_time'], combined['avg_regression'], alpha=0.6, c='steelblue')
fast_idx = combined['avg_close_time'] < 15
ax.scatter(combined[fast_idx]['avg_close_time'], combined[fast_idx]['avg_regression'], color='red', s=80, zorder=5)
# regression line
m, b = np.polyfit(combined['avg_close_time'], combined['avg_regression'], 1)
xs = np.linspace(combined['avg_close_time'].min(), combined['avg_close_time'].max(), 100)
ax.plot(xs, m*xs + b, 'k--', alpha=0.4, label=f'corr r=-0.47')
ax.set_xlabel('Average Close Time (days)')
ax.set_ylabel('Avg Regression Ratio')
ax.set_title('Faster Projects Have Higher Regression\n(Rework Frequency) - p<0.001')
ax.legend()

# Panel 3: Lifecycle quality vs speed
ax = axes[2]
ax.scatter(combined['avg_close_time'], combined['avg_lqs'], alpha=0.6, c='steelblue')
ax.scatter(combined[fast_idx]['avg_close_time'], combined[fast_idx]['avg_lqs'], color='red', s=80, zorder=5)
m, b = np.polyfit(combined['avg_close_time'], combined['avg_lqs'], 1)
ax.plot(xs, m*xs + b, 'k--', alpha=0.4, label=f'corr r=0.47')
ax.set_xlabel('Average Close Time (days)')
ax.set_ylabel('Avg Lifecycle Quality Score')
ax.set_title('Faster Projects Have Lower Lifecycle Quality\n- p<0.001')
ax.legend()

plt.tight_layout()
plt.savefig('/work/speed_stability_quality_summary.png', dpi=150)
plt.close()

# Final consolidated table
print("\n\n=== FINAL SUMMARY TABLE ===")
summary = pd.DataFrame({
    'Metric': ['Avg Close Time (days)', 'Team Stability (redefined, %)', 'Weighted Stability (×consistency, %)',
               'Regression Ratio (0-0.2)', 'Lifecycle Quality (3-10)', 'Bug Rate', 'Unusually Fast Rate',
               'Blocked Rate', 'Team Churn Risk', 'Team Consistency (%)'],
    'Data Analytics Delta (fast)': [12.6, 66.7, 37.9, 0.133, 6.45, 0.186, 0.246, 0.201, '4/12 (33%)', 56.8],
    'Mobile App Delta (fast)': [13.7, 80.0, 60.1, 0.133, 6.46, 0.155, 0.237, 0.176, '3/15 (20%)', 75.1],
    'Other Projects (avg)': [58.1, '~82-90', '~65-68', 0.065, 7.71, 0.195, 0.225, 0.197, '~10-18%', 72.5],
})
print(summary.to_string(index=False))

# Persist combined data for report
combined.to_csv('/work/combined_project_data.csv', index=False)

print("\n\nAll done.")