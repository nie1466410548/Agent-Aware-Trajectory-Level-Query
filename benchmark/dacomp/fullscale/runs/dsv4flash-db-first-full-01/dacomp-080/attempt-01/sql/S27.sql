SELECT
  CASE WHEN location_latitude > 0 AND location_longitude < -30 THEN 'AMERICAS'
       WHEN location_latitude <= 0 AND location_longitude < -30 THEN 'AMERICAS'
       WHEN location_latitude > 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'EUROPE'
       WHEN location_latitude <= 35 AND location_longitude >= -30 AND location_longitude < 60 THEN 'AFRICA/MIDEAST'
       WHEN location_longitude >= 60 AND location_longitude < 180 THEN 'ASIA/OCEANIA'
       ELSE 'OTHER' END AS rough_region,
  COUNT(*) AS n
FROM qualtrics__response
GROUP BY rough_region