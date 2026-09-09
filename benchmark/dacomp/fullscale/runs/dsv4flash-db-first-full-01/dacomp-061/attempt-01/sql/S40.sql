
    SELECT 
        CASE WHEN regression_ratio = 0.0 THEN 'No Regression'
             WHEN regression_ratio = 0.1 THEN 'Some Regression'
             ELSE 'High Regression'
        END as regression_level,
        COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics 
    WHERE project_name NOT IN ('Data Analytics Delta', 'Mobile App Delta')
    GROUP BY regression_ratio
    ORDER BY regression_ratio
