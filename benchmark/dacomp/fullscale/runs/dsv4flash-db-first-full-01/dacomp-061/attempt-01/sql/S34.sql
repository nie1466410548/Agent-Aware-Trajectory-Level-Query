
    SELECT project_name,
        AVG(regression_ratio) as avg_regression,
        AVG(lifecycle_quality_score) as avg_lqs,
        AVG(lifecycle_deviation_ratio) as avg_deviation,
        AVG(total_risk_score) as avg_risk,
        AVG(intelligence_score) as avg_intel,
        AVG(completion_probability) as avg_cp,
        SUM(CASE WHEN lifecycle_outlier_status='Unusually Fast' THEN 1 ELSE 0 END)*1.0/COUNT(*) as unusually_fast_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Statistical Outlier' THEN 1 ELSE 0 END)*1.0/COUNT(*) as stat_outlier_rate,
        SUM(CASE WHEN lifecycle_outlier_status='Above Normal Range' THEN 1 ELSE 0 END)*1.0/COUNT(*) as above_normal_rate,
        SUM(CASE WHEN current_status='Blocked' THEN 1 ELSE 0 END)*1.0/COUNT(*) as blocked_rate,
        SUM(CASE WHEN issue_type='Bug' THEN 1 ELSE 0 END)*1.0/COUNT(*) as bug_rate
    FROM jira__issue_intelligence_analytics
    GROUP BY project_name
