
    SELECT p.project_name, p.avg_close_time, i.avg_regression, i.avg_lqs
    FROM (SELECT project_name, AVG(avg_close_time_days) as avg_close_time FROM jira__project_enhanced GROUP BY project_name) p
    JOIN (SELECT project_name, AVG(regression_ratio) as avg_regression, AVG(lifecycle_quality_score) as avg_lqs FROM jira__issue_intelligence_analytics GROUP BY project_name) i
    ON p.project_name = i.project_name
