SELECT job_stage, COUNT(*) AS n, AVG(technical_score) AS avg_tech, AVG(problem_solving_score) AS avg_ps,
       AVG(communication_score) AS avg_comm, AVG(leadership_score) AS avg_lead
FROM greenhouse__interview_enhanced
GROUP BY job_stage
ORDER BY n DESC