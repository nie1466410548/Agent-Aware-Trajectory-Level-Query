SELECT COUNT(DISTINCT interviewer_name) as unique_interviewers,
       COUNT(DISTINCT interview_id) as unique_interviews
FROM greenhouse__interview_enhanced