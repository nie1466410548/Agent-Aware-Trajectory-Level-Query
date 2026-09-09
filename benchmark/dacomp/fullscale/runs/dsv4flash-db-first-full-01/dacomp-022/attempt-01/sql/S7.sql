SELECT "Vehicle Type",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Ride Distance"), 2) as avg_distance,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"), 2) as avg_driver_rating,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Vehicle Type"
ORDER BY avg_fare_per_km DESC