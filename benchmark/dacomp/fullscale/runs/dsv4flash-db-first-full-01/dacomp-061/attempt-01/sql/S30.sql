
    SELECT project_id, project_name, project_key, project_lead_user_name, 
           avg_close_time_days, median_close_time_days, count_closed_issues, count_open_issues,
           avg_age_currently_open_days, avg_assigned_close_time_days
    FROM jira__project_enhanced 
    WHERE avg_close_time_days < 15
    ORDER BY avg_close_time_days
