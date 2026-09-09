SELECT COUNT(*) as total,
       SUM(CASE WHEN avg_interview_score IS NOT NULL THEN 1 ELSE 0 END) as with_score
FROM greenhouse__candidate_summary