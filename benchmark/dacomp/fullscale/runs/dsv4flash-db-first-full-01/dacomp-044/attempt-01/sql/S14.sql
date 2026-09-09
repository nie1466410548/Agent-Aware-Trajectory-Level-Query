SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format
ORDER BY n DESC