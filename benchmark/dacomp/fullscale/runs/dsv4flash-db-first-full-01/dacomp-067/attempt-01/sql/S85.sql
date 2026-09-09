
SELECT rating, COUNT(*) as cnt
FROM greenhouse__interview_scorecard_detail
WHERE rating IS NOT NULL
GROUP BY rating
ORDER BY rating
