
    SELECT project_name, AVG(avg_close_time_days) as avg_close, MIN(avg_close_time_days) as min_close
    FROM jira__project_enhanced
    GROUP BY project_name
