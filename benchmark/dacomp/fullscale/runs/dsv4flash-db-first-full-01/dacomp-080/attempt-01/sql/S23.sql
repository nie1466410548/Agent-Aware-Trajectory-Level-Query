SELECT n_channels_in_resp, COUNT(*) AS n_survey_responses
FROM (
  SELECT survey_response_id, COUNT(DISTINCT distribution_channel) AS n_channels_in_resp
  FROM qualtrics__response
  GROUP BY survey_response_id
) t
GROUP BY n_channels_in_resp