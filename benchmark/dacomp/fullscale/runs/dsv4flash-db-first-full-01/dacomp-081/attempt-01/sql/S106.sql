
    SELECT survey_id, question_type, COUNT(*) as cnt
    FROM qualtrics__response
    GROUP BY survey_id, question_type
    HAVING COUNT(*) >= 10
    ORDER BY cnt DESC
    LIMIT 20
