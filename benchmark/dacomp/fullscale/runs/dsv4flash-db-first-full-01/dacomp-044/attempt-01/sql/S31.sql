SELECT
  "Key Locations (School/Hospital/Community)" AS location,
  COUNT(*) AS n,
  ROUND(100.0 * SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END)/COUNT(*),1) AS both_sig_pct,
  SUM(CASE WHEN "Behavioral Change Assessment"='Significant' AND "Effectiveness Tracking"='Significant' THEN 1 ELSE 0 END) AS both_sig_n
FROM health_education
WHERE "Population Covered" = 'Student'
GROUP BY location
ORDER BY both_sig_pct DESC