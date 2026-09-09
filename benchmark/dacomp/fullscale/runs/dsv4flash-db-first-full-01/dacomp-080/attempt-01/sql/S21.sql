SELECT MIN(survey_progress) AS min_p, MAX(survey_progress) AS max_p, AVG(survey_progress) AS avg_p,
MIN(duration_in_seconds) AS min_d, MAX(duration_in_seconds) AS max_d, AVG(duration_in_seconds) AS avg_d
FROM qualtrics__response