
import pandas as pd, numpy as np

# Load target cohort full profile
prof = db.frame(db.query("""
SELECT * FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
"""))
print("Target cohort size:", len(prof))
print(prof[['engagement_depth_score','engagement_breadth_score','engagement_quality_score','engagement_impact_score',
            'total_outbound_influence','total_inbound_influence','issues_assigned','issues_reported',
            'direct_network_connections','cross_functional_projects','strategic_value_score','total_engagement_score']].describe().T[['mean','std','min','max']])
