SELECT 
  CASE WHEN "Ride Distance" <= 5 THEN '0-5 km'
       WHEN "Ride Distance" <= 10 THEN '5-10 km'
       WHEN "Ride Distance" <= 15 THEN '10-15 km'
       WHEN "Ride Distance" <= 20 THEN '15-20 km'
       WHEN "Ride Distance" <= 25 THEN '20-25 km'
       WHEN "Ride Distance" <= 30 THEN '25-30 km'
       WHEN "Ride Distance" <= 40 THEN '30-40 km'
       ELSE '40+ km' END as distance_band,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY distance_band
ORDER BY MIN("Ride Distance")