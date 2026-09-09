SELECT 
  CASE WHEN "Voice Talk Average Time" < 5 THEN '0-5 min'
       WHEN "Voice Talk Average Time" < 10 THEN '5-10 min'
       WHEN "Voice Talk Average Time" < 15 THEN '10-15 min'
       ELSE '15+ min' END as voice_band,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value"/NULLIF("Ride Distance",0)),2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"),2) as avg_driver_rating
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY voice_band
ORDER BY MIN("Voice Talk Average Time")