SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' THEN 1 ELSE 0 END) AS behav_sig,
  SUM(CASE WHEN "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS track_sig,
  SUM(CASE WHEN "Effectiveness Assessment"='Significant' THEN 1 ELSE 0 END) AS eff_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location