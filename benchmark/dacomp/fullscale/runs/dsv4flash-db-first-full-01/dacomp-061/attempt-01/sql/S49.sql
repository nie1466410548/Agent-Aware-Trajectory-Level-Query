
    SELECT user_display_name, total_assigned_issues, resolved_issues, at_churn_risk,
           consistency_percentage, avg_resolution_days, bug_issues, overall_performance_score,
           estimate_accuracy_percentage
    FROM jira__team_performance_dashboard
    WHERE project_name = 'Mobile App Delta'
    ORDER BY at_churn_risk DESC
