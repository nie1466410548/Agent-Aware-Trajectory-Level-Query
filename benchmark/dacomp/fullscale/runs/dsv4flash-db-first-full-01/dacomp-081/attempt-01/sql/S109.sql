
    SELECT value, sub_question_text, question_option_key, sub_question_key,
           user_language, question_type, question_id
    FROM qualtrics__response
    WHERE sub_question_text IS NOT NULL
    LIMIT 50000
