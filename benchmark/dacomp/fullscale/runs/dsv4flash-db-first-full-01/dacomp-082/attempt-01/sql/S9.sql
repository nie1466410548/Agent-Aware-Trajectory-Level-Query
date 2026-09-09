SELECT project_category,
       SUM(count_email_survey_responses) AS email_responses,
       SUM(count_email_completed_survey_responses) AS email_completed,
       SUM(count_sms_survey_responses) AS sms_responses,
       SUM(count_sms_completed_survey_responses) AS sms_completed,
       SUM(count_social_media_survey_responses) AS social_responses,
       SUM(count_social_media_completed_survey_responses) AS social_completed,
       SUM(count_personal_link_survey_responses) AS personal_link_responses,
       SUM(count_personal_link_completed_survey_responses) AS personal_link_completed,
       SUM(count_qr_code_survey_responses) AS qr_responses,
       SUM(count_qr_code_completed_survey_responses) AS qr_completed,
       SUM(count_anonymous_survey_responses) AS anon_responses,
       SUM(count_anonymous_completed_survey_responses) AS anon_completed,
       SUM(count_uncategorized_survey_responses) AS uncat_responses,
       SUM(count_uncategorized_completed_survey_responses) AS uncat_completed
FROM qualtrics__survey
GROUP BY project_category