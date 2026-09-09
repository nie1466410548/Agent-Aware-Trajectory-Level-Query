
    SELECT 
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity,
        AVG(collaboration_opportunity_score) as avg_collab,
        AVG(efficiency_opportunity_score) as avg_efficiency,
        AVG(process_opportunity_score) as avg_process_opp
    FROM jira__issue_intelligence_analytics
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
