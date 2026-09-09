
    SELECT 
        CASE WHEN project_name IN ('Data Analytics Delta', 'Mobile App Delta') THEN 'Fast Projects' ELSE 'Other Projects' END as project_group,
        lifecycle_quality_score,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY project_group, lifecycle_quality_score
    ORDER BY project_group, lifecycle_quality_score
