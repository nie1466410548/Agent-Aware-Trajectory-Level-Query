SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  "Campaign Content (Prevention/Treatment/Policy)" AS content,
  COUNT(*) AS n,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location, content
ORDER BY format, location