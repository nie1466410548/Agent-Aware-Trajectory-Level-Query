SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  ROUND(100.0*SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS both_pct
FROM health_education
WHERE "Population Covered" != 'Student'
GROUP BY format, location
ORDER BY both_pct DESC