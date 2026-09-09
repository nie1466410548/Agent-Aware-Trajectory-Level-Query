import pandas as pd, numpy as np

prof = db.frame(db.query("""
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
    COUNT(DISTINCT survey_id) AS n_distinct_surveys,
    COUNT(DISTINCT CASE WHEN is_finished_with_survey=1 THEN survey_response_id END) AS n_completed,
    COUNT(DISTINCT distribution_channel) AS n_channels,
    COUNT(DISTINCT date(survey_response_recorded_at)) AS n_active_days,
    AVG(survey_progress) AS avg_progress,
    AVG(duration_in_seconds) AS avg_duration,
    AVG(location_latitude) AS avg_lat,
    AVG(location_longitude) AS avg_lon,
    MIN(survey_response_recorded_at) AS first_response_at,
    MAX(survey_response_recorded_at) AS last_response_at
  FROM qualtrics__response
  GROUP BY recipient_email
)
SELECT u.*, l.dom_lang,
  1.0*u.n_completed/u.n_survey_responses AS completion_rate,
  (julianday(u.last_response_at) - julianday(u.first_response_at))/30.44 AS active_months
FROM user_agg u
LEFT JOIN lang_mode l ON l.recipient_email = u.email
ORDER BY u.n_survey_responses DESC
"""))

print(prof.shape)
print(prof.dtypes)
print(prof.describe().T)
prof.to_csv('/work/user_profile.csv', index=False)
