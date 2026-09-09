SELECT 
  MIN(n_survey_responses) AS min_n,
  MAX(n_survey_responses) AS max_n,
  AVG(n_survey_responses) AS avg_n,
  MIN(n_completed) AS min_c,
  MAX(n_completed) AS max_c,
  AVG(n_completed) AS avg_c,
  MIN(completion_rate) AS min_cr,
  MAX(completion_rate) AS max_cr,
  AVG(completion_rate) AS avg_cr,
  MIN(n_channels) AS min_ch,
  MAX(n_channels) AS max_ch,
  AVG(n_channels) AS avg_ch,
  MIN(avg_progress) AS min_p,
  MAX(avg_progress) AS max_p,
  AVG(avg_progress) AS avg_p
FROM (
  WITH lang_mode AS (
    SELECT recipient_email, user_language AS dom_lang
    FROM (
      SELECT recipient_email, user_language,
             ROW_NUMBER() OVER (PARTITION BY recipient_email ORDER BY COUNT(*) DESC) AS rn
      FROM qualtrics__response
      GROUP BY recipient_email, user_language
    )
    WHERE rn = 1
  ),
  user_agg AS (
    SELECT
      recipient_email AS email,
      COUNT(DISTINCT survey_response_id) AS n_survey_responses,
      COUNT(DISTINCT CASE WHEN is_finished_with_survey=1 THEN survey_response_id END) AS n_completed,
      COUNT(DISTINCT distribution_channel) AS n_channels,
      AVG(survey_progress) AS avg_progress
    FROM qualtrics__response
    GROUP BY recipient_email
  )
  SELECT u.*, 1.0*u.n_completed/u.n_survey_responses AS completion_rate
  FROM user_agg u
)