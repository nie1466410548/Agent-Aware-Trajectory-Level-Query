SELECT i.technical_score, a.candidate_company, COUNT(*) AS n
FROM greenhouse__interview_enhanced i
JOIN greenhouse__application_enhanced a ON a.application_id = i.application_id
WHERE i.technical_score IS NOT NULL
GROUP BY i.technical_score, a.candidate_company
ORDER BY a.candidate_company, i.technical_score
LIMIT 30