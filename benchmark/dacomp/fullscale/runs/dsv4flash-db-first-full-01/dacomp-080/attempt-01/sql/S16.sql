SELECT COUNT(DISTINCT recipient_email) AS n_resp_emails, COUNT(DISTINCT survey_response_id) AS n_survey_resp
FROM qualtrics__response