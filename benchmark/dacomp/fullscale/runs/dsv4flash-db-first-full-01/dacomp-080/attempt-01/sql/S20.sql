SELECT survey_response_id, recipient_email, distribution_channel, survey_progress, duration_in_seconds, is_finished_with_survey, survey_response_status, user_language, location_latitude, location_longitude
FROM qualtrics__response
WHERE recipient_email='melissawilliams@example.com'
LIMIT 20