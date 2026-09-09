
    SELECT survey_response_id, COUNT(*) as n_questions
    FROM qualtrics__response
    GROUP BY survey_response_id
    ORDER BY n_questions DESC
    LIMIT 20
