SELECT interview_scorecard_key, COUNT(*) AS n
FROM greenhouse__interview_enhanced
GROUP BY interview_scorecard_key
ORDER BY n DESC LIMIT 10