
    SELECT 
        CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END as project_group,
        AVG(age_risk_score) as avg_age_risk,
        AVG(process_risk_score) as avg_process_risk,
        AVG(complexity_risk_score) as avg_complexity_risk,
        AVG(engagement_risk_score) as avg_engagement_risk,
        AVG(assignment_risk_score) as avg_assignment_risk,
        AVG(deviation_risk_score) as avg_deviation_risk,
        AVG(total_risk_score) as avg_total_risk,
        AVG(total_opportunity_score) as avg_opportunity
    FROM jira__issue_intelligence_analytics
    GROUP BY project_group
