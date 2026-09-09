SELECT 
  MIN(total_count_surveys) AS min_surveys,
  AVG(total_count_surveys) AS avg_surveys,
  MAX(total_count_surveys) AS max_surveys,
  MIN(total_count_completed_surveys) AS min_completed,
  AVG(total_count_completed_surveys) AS avg_completed,
  MAX(total_count_completed_surveys) AS max_completed,
  MIN(avg_survey_progress_pct) AS min_progress,
  AVG(avg_survey_progress_pct) AS avg_progress,
  MAX(avg_survey_progress_pct) AS max_progress,
  MIN(avg_survey_duration_in_seconds) AS min_duration,
  AVG(avg_survey_duration_in_seconds) AS avg_duration,
  MAX(avg_survey_duration_in_seconds) AS max_duration
FROM qualtrics__contact