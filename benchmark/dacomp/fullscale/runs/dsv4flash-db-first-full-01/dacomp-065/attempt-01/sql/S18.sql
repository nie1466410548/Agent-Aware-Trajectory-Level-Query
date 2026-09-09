SELECT candidate_company, COUNT(*) AS n, 
       AVG(technical_score) AS avg_tech_score,
       AVG(problem_solving_score) AS avg_prob_solving,
       AVG(communication_score) AS avg_comm_score,
       AVG(overall_recommendation IN ('strong_yes','yes')) AS hire_rec_rate
FROM greenhouse__interview_enhanced
WHERE technical_score IS NOT NULL
GROUP BY candidate_company
ORDER BY n DESC