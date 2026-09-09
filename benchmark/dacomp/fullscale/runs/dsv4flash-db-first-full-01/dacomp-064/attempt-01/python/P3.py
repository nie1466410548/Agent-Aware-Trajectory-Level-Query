
import pandas as pd, numpy as np
from scipy import stats

prof_all = db.frame(db.query("""
SELECT *, 
  CASE WHEN engagement_impact_score >= 3 AND cross_functional_projects >= 3 THEN 1 ELSE 0 END AS is_target
FROM jira__stakeholder_engagement_insights
"""))
prof_all['influence_imbalance'] = prof_all['total_outbound_influence'] - prof_all['total_inbound_influence']
prof_all['assign_report_ratio'] = prof_all['issues_assigned'] / prof_all['issues_reported'].replace(0, np.nan)

target = prof_all[prof_all['is_target']==1]
other = prof_all[prof_all['is_target']==0]

metrics = ['engagement_depth_score','engagement_breadth_score','engagement_quality_score',
           'total_outbound_influence','total_inbound_influence','influence_imbalance',
           'issues_assigned','issues_reported','assign_report_ratio',
           'direct_network_connections','strategic_value_score','total_engagement_score']

print("=== Target vs Non-Target comparison (Mann-Whitney U) ===")
print(f"{'Metric':<28}{'Target':>10}{'Other':>10}{'p-value':>10}")
for m in metrics:
    t = target[m].dropna(); o = other[m].dropna()
    stat, p = stats.mannwhitneyu(t, o, alternative='two-sided')
    print(f"{m:<28}{t.mean():>10.2f}{o.mean():>10.2f}{p:>10.2e}")

# Response pattern distribution comparison
print("\n=== Response pattern distribution: Target vs Other (share) ===")
rp = prof_all.groupby(['response_pattern_type','is_target']).size().unstack(fill_value=0)
rp['target_share'] = rp[1]/(rp[1]+rp[0])
print(rp.sort_values('target_share', ascending=False).head(10))
print("\nBottom share patterns:")
print(rp.sort_values('target_share').head(10))

# Strategic value vs actual contribution: regression within target
# contribution proxies: issues_assigned, total_comments_authored, issues_reported
prof = prof_all[prof_all['is_target']==1].copy()
print("\n=== Within target: correlation of strategic_value with contribution proxies ===")
for m in ['issues_assigned','issues_reported','total_comments_authored','engagement_quality_score','total_engagement_score','direct_network_connections']:
    print(f"strategic_value vs {m}: {prof['strategic_value_score'].corr(prof[m]):.3f}")

# Risk status within target by breadth quartile
prof['breadth_q'] = pd.qcut(prof['engagement_breadth_score'], 4, labels=['Q1(18-26)','Q2(27-31)','Q3(32-40)','Q4(41-50)'])
risk_pivot = prof.groupby('breadth_q', observed=True).apply(
    lambda g: pd.Series({
        'n': len(g),
        'avg_depth': g['engagement_depth_score'].mean(),
        'avg_breadth': g['engagement_breadth_score'].mean(),
        'at_risk_share': (g['engagement_risk_status'].isin(['At Risk','Disengaged'])).mean(),
        'avg_imbalance': g['influence_imbalance'].mean(),
        'avg_assign_ratio': g['assign_report_ratio'].mean()
    }), include_groups=False)
print("\n=== Target cohort by breadth quartile ===")
print(risk_pivot.round(2))
