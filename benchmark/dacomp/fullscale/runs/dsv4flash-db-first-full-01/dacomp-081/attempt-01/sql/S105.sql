
    SELECT survey_response_id, survey_id, question_id, question_text, 
           question_type, value, response_text, sub_question_key,
           sub_question_text, question_option_key, user_language,
           contact_language, embedded_data
    FROM qualtrics__response
    WHERE survey_response_id = 'SUR10008772252'
    ORDER BY question_id
