SELECT sourced_from,
       ROUND(AVG(count_interviews), 2) as avg_interviews,
       ROUND(AVG(count_distinct_interviewers), 2) as avg_interviewers,
       SUM(CASE WHEN has_interviewed_w_hiring_manager = 1 THEN 1 ELSE 0 END) as interviewed_with_hm,
       COUNT(*) as total_with_interview_data
FROM greenhouse__application_enhanced 
WHERE count_interviews > 0
GROUP BY sourced_from