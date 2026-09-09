SELECT 
  CASE WHEN "Driver Ratings" < 3.5 THEN '3.0-3.4'
       WHEN "Driver Ratings" < 4.0 THEN '3.5-3.9'
       WHEN "Driver Ratings" < 4.5 THEN '4.0-4.4'
       ELSE '4.5-5.0' END as rating_band,
       COUNT(*) as rides,
       ROUND(SUM("Booking Value"),2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY rating_band
ORDER BY MIN("Driver Ratings")