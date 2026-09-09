
    SELECT lifecycle_quality_score, COUNT(*) as cnt
    FROM jira__issue_intelligence_analytics
    GROUP BY lifecycle_quality_score
    ORDER BY lifecycle_quality_score
