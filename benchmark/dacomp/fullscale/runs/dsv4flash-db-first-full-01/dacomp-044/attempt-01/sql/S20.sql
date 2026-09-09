SELECT
  "Campaign Format (Poster/Video/Lecture)" AS format,
  "Key Locations (School/Hospital/Community)" AS location,
  ROUND(AVG("Campaign Frequency (times/month)"),1) AS avg_freq,
  ROUND(AVG("Distribution Quantity"),0) AS avg_qty,
  ROUND(AVG(CAST(REPLACE("Knowledge Assessment",'%','') AS REAL)),1) AS avg_knowledge
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY format, location
ORDER BY format, location