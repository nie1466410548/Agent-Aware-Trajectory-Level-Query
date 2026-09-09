
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Population Covered" AS pop,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track
FROM health_education
WHERE "Population Covered" != 'Student'
