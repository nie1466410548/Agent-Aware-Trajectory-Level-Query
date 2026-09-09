SELECT application_id, interview_id, interviewer_user_id, COUNT(*) AS n
FROM greenhouse__interview_enhanced
GROUP BY application_id, interview_id, interviewer_user_id
ORDER BY n DESC LIMIT 10