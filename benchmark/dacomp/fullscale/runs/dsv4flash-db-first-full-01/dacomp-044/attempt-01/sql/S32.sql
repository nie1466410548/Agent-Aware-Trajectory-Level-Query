
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty
FROM health_education
WHERE "Population Covered" = 'Student'
