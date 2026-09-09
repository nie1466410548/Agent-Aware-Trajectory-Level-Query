SELECT COUNT(*) as total_interviews, 
       COUNT(DISTINCT interview_id) as unique_interviews,
       AVG(duration_interview_minutes) as avg_duration,
       overall_recommendation,
       COUNT(*) as cnt
FROM greenhouse__interview_enhanced 
WHERE overall_recommendation IS NOT NULL
GROUP BY overall_recommendation
ORDER BY cnt DESC