SELECT "Drop Location",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Drop Location"
ORDER BY avg_fare_per_km DESC
LIMIT 10