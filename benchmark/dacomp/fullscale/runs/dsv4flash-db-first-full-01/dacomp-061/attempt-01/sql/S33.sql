
    SELECT 
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        AVG(total_risk_score) as avg_risk,
        AVG(intelligence_score) as avg_intel,
        AVG(completion_probability) as avg_cp
    FROM jira__issue_intelligence_analytics
