SELECT
  CASE WHEN instr("New Media Metrics (Views/Shares)",'/')>0
       THEN CAST(substr("New Media Metrics (Views/Shares)",1,instr("New Media Metrics (Views/Shares)",'/')-1) AS INTEGER) END AS views,
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  "Behavioral Change Assessment" AS behav,
  "Effectiveness Tracking" AS track
FROM health_education
WHERE "Population Covered" = 'Student'
  AND "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant'