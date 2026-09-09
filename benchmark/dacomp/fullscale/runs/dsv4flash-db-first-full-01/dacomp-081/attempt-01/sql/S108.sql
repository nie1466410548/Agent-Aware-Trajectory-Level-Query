
    SELECT question_text, COUNT(*) as cnt
    FROM qualtrics__response
    GROUP BY question_text
    ORDER BY cnt DESC
    LIMIT 30
