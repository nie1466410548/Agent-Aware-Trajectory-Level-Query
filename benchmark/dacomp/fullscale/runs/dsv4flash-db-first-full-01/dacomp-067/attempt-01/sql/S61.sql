
SELECT source_name, source_type, total_applications, unique_candidates, 
       total_hires, applications_with_interviews, avg_process_days,
       hire_rate, interview_rate, interview_to_hire_rate, efficiency_score
FROM greenhouse__talent_pipeline_simplified
ORDER BY source_name
