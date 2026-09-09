SELECT 
  SUM(CASE WHEN location_latitude IS NOT NULL THEN 1 ELSE 0 END) AS with_lat,
  SUM(CASE WHEN ip_address IS NOT NULL THEN 1 ELSE 0 END) AS with_ip,
  SUM(CASE WHEN recipient_email IS NOT NULL THEN 1 ELSE 0 END) AS with_email,
  COUNT(*) AS total
FROM qualtrics__response