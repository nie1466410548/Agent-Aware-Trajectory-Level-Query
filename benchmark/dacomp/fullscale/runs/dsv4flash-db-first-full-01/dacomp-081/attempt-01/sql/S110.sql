
    SELECT survey_id, user_language, COUNT(*) AS n, AVG(value) AS avg_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 2
