SELECT "Driver Ratings",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings,
       ROUND(100.0*COUNT(*)/SUM(COUNT(*)) OVER (), 2) as pct_of_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Driver Ratings"
ORDER BY "Driver Ratings"