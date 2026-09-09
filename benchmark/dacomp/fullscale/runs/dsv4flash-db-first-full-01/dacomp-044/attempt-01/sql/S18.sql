SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS behav_sig_pct,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
  ROUND(100.0 * SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS track_sig_pct,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) / COUNT(*), 1) AS both_sig_pct
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY both_sig_pct DESC, n DESC