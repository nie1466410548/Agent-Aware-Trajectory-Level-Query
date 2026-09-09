
    SELECT 
        issue_type,
        COUNT(*) as cnt,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(total_lifecycle_days) as avg_lifecycle_days,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        AVG(total_risk_score) as avg_risk
    FROM jira__issue_intelligence_analytics 
    WHERE project_name = 'Data Analytics Delta'
    GROUP BY issue_type
    ORDER BY cnt DESC
