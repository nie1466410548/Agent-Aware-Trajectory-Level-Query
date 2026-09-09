SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY both_sig DESC, n DESC