
    SELECT 
        regression_ratio,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio
