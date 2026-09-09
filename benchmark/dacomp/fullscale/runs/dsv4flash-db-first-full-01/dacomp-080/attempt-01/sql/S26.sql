SELECT 
  ROUND(location_latitude/10)*10 AS lat_bin,
  ROUND(location_longitude/20)*20 AS lon_bin,
  COUNT(*) AS n_rows
FROM qualtrics__response
GROUP BY lat_bin, lon_bin
ORDER BY n_rows DESC
LIMIT 30