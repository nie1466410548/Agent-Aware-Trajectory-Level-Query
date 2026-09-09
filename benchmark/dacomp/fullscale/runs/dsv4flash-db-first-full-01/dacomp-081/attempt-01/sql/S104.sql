
    SELECT survey_id, user_language, COUNT(*) AS n, 
           AVG(value) AS avg_v, MIN(value) AS min_v, MAX(value) AS max_v
    FROM qualtrics__response
    GROUP BY survey_id, user_language
    HAVING n >= 3
