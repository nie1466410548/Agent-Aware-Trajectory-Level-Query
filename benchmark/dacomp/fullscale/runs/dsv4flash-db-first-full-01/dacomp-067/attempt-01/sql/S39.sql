SELECT interviewer_is_hiring_manager, COUNT(*) as cnt,
       AVG(duration_interview_minutes) as avg_duration
FROM greenhouse__interview_enhanced
GROUP BY interviewer_is_hiring_manager