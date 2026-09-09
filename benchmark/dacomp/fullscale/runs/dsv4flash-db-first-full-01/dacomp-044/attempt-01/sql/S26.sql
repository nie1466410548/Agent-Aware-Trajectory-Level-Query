
SELECT "Campaign Format (Poster/Video/Lecture)" AS format,
       "Key Locations (School/Hospital/Community)" AS location,
       "Campaign Content (Prevention/Treatment/Policy)" AS content,
       "Behavioral Change Assessment" AS behav,
       "Effectiveness Tracking" AS track,
       "Effectiveness Assessment" AS eff,
       "Campaign Frequency (times/month)" AS freq,
       "Distribution Quantity" AS qty,
       "Awareness Rate Survey" AS awareness,
       "Knowledge Assessment" AS knowledge,
       "New Media Metrics (Views/Shares)" AS new_media
FROM health_education
WHERE "Population Covered" = 'Student'
