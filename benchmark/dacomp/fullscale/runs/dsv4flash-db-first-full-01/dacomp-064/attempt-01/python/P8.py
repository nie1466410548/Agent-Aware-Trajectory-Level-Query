
import pandas as pd, numpy as np
from scipy import stats

prof = db.frame(db.query("""
SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
"""))
prof['influence_imbalance'] = prof['total_outbound_influence'] - prof['total_inbound_influence']
prof['influence_ratio'] = prof['total_outbound_influence'] / prof['total_inbound_influence'].replace(0,1)
prof['depth_breadth_ratio'] = prof['engagement_depth_score'] / prof['engagement_breadth_score']

# Spearman correlations with depth
print("=== Spearman correlations with engagement_depth_score (target cohort) ===")
for m in ['engagement_breadth_score','total_outbound_influence','total_inbound_influence','influence_imbalance',
          'direct_network_connections','cross_functional_projects','total_projects_involved','strategic_value_score',
          'engagement_quality_score','issues_assigned','issues_reported','total_comments_authored']:
    r, p = stats.spearmanr(prof['engagement_depth_score'], prof[m])
    print(f"depth vs {m:<32} r={r:+.3f} p={p:.2e}")

print("\n=== Spearman correlations with influence_imbalance ===")
for m in ['engagement_breadth_score','direct_network_connections','cross_functional_projects','total_projects_involved','strategic_value_score']:
    r, p = stats.spearmanr(prof['influence_imbalance'], prof[m])
    print(f"imbalance vs {m:<32} r={r:+.3f} p={p:.2e}")

# Define the strongest 'phenomenon' signature: breadth > 40 (top quartile), depth <= 20, influence imbalance > 10
signature = (prof['engagement_breadth_score'] >= 40) & (prof['engagement_depth_score'] <= 20) & (prof['influence_imbalance'] > 10)
sub = prof[signature]
print(f"\n=== Strong-phenomenon sub-cohort: {len(sub)} of {len(prof)} ({len(sub)/len(prof)*100:.1f}%) ===")
print(f"Avg depth: {sub['engagement_depth_score'].mean():.2f}, breadth: {sub['engagement_breadth_score'].mean():.2f}")
print(f"Avg imbalance: {sub['influence_imbalance'].mean():.2f}, connections: {sub['direct_network_connections'].mean():.1f}")
print(f"At-risk share: {(sub['engagement_risk_status'].isin(['At Risk','Disengaged'])).mean()*100:.1f}%")
print(f"Avg strategic value: {sub['strategic_value_score'].mean():.1f}")

# Response pattern of the strong sub-cohort
print("\n=== Response pattern distribution in strong sub-cohort ===")
rp_strong = sub['response_pattern_type'].value_counts(normalize=True).head(6).round(3)
rp_all = prof['response_pattern_type'].value_counts(normalize=True)
enrich = pd.DataFrame({'strong_share': rp_strong, 'overall_share': rp_all}).fillna(0)
enrich['enrichment'] = (enrich['strong_share']/enrich['overall_share']).round(2)
print(enrich.sort_values('enrichment', ascending=False))

# Impact of the strong sub-cohort on projects they touch
print("\n=== Top risk-stakeholders (impact score 5, at risk, high strategic value) ===")
top_risk = prof[(prof['engagement_impact_score']==5) & (prof['engagement_risk_status'].isin(['At Risk','Disengaged']))].sort_values('strategic_value_score', ascending=False)
print(f"Count: {len(top_risk)}")
print(top_risk[['user_display_name','strategic_value_score','engagement_depth_score','engagement_breadth_score','influence_imbalance','response_pattern_type','stakeholder_archetype','development_opportunity']].head(10))
