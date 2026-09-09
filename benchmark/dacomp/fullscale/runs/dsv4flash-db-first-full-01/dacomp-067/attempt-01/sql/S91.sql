SELECT interview_name, status, COUNT(*) as cnt
FROM greenhouse__interview_enhanced
GROUP BY interview_name, status
ORDER BY interview_name, status