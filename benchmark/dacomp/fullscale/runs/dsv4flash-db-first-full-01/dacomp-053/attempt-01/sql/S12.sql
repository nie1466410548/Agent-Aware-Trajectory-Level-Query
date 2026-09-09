SELECT health_grade, 
       ROUND(AVG(team_size_category),2) as avg_team_size,
       ROUND(AVG(complexity_factor),4) as avg_complexity,
       ROUND(AVG(collaboration_score),2) as avg_collab,
       ROUND(AVG(management_priority),2) as avg_priority
FROM asana__project_analytics
GROUP BY health_grade ORDER BY health_grade