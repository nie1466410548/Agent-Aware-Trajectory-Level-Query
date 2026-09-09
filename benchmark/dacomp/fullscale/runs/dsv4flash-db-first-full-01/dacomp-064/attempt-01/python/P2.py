import pandas as pd, numpy as np, matplotlib.pyplot as plt, seaborn as sns

prof = db.frame(db.query("""
SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
"""))

# Compute derived metrics
prof['influence_imbalance'] = prof['total_outbound_influence'] - prof['total_inbound_influence']
prof['assign_report_ratio'] = prof['issues_assigned'] / prof['issues_reported'].replace(0, np.nan)
prof['depth_breadth_ratio'] = prof['engagement_depth_score'] / prof['engagement_breadth_score']

# Correlation matrix of key metrics
key_cols = ['engagement_depth_score','engagement_breadth_score','engagement_quality_score',
            'total_outbound_influence','total_inbound_influence','influence_imbalance',
            'issues_assigned','issues_reported','assign_report_ratio',
            'direct_network_connections','cross_functional_projects','strategic_value_score',
            'total_engagement_score','depth_breadth_ratio']

corr = prof[key_cols].corr()

plt.figure(figsize=(14,12))
sns.heatmap(corr, annot=True, fmt='.2f', cmap='RdBu_r', center=0, square=True)
plt.title('Correlation Matrix: Target Stakeholder Metrics', fontsize=14)
plt.tight_layout()
plt.savefig('/work/correlation_matrix.png', dpi=150)
plt.close()

# Scatter: Depth vs Breadth colored by risk status
plt.figure(figsize=(10,6))
risk_colors = {'Healthy Engagement':'green','Highly Engaged':'blue','At Risk':'orange','Disengaged':'red','Recently Joined':'purple'}
for risk in ['Healthy Engagement','Highly Engaged','At Risk']:
    mask = prof['engagement_risk_status']==risk
    plt.scatter(prof.loc[mask,'engagement_breadth_score'], prof.loc[mask,'engagement_depth_score'], 
                c=risk_colors.get(risk,'gray'), label=risk, alpha=0.6, s=30)
plt.xlabel('Engagement Breadth Score', fontsize=12)
plt.ylabel('Engagement Depth Score', fontsize=12)
plt.title('Target Cohort: Depth vs Breadth by Risk Status', fontsize=13)
plt.legend()
plt.tight_layout()
plt.savefig('/work/depth_vs_breadth.png', dpi=150)
plt.close()

# Influence imbalance distribution
plt.figure(figsize=(10,6))
plt.hist(prof['influence_imbalance'], bins=30, edgecolor='black', alpha=0.7)
plt.axvline(prof['influence_imbalance'].mean(), color='red', linestyle='--', label=f"Mean: {prof['influence_imbalance'].mean():.2f}")
plt.xlabel('Influence Imbalance (Outbound - Inbound)', fontsize=12)
plt.ylabel('Count', fontsize=12)
plt.title('Target Cohort: Influence Imbalance Distribution', fontsize=13)
plt.legend()
plt.tight_layout()
plt.savefig('/work/influence_imbalance.png', dpi=150)
plt.close()

print("Depth vs Breadth correlation:", corr.loc['engagement_depth_score','engagement_breadth_score'])
print("Depth vs Influence Imbalance:", corr.loc['engagement_depth_score','influence_imbalance'])
print("Breadth vs Influence Imbalance:", corr.loc['engagement_breadth_score','influence_imbalance'])
print("Depth vs Strategic Value:", corr.loc['engagement_depth_score','strategic_value_score'])
print("Breadth vs Strategic Value:", corr.loc['engagement_breadth_score','strategic_value_score'])
print("Depth vs Assign/Report Ratio:", corr.loc['engagement_depth_score','assign_report_ratio'])
print("Breadth vs Assign/Report Ratio:", corr.loc['engagement_breadth_score','assign_report_ratio'])
print("Influence Imbalance vs Assign/Report Ratio:", corr.loc['influence_imbalance','assign_report_ratio'])