SELECT "Vehicle Type",
       COUNT(*) as completed_rides,
       ROUND(SUM("Booking Value"), 2) as total_earnings,
       ROUND(AVG("Booking Value"), 2) as avg_per_ride,
       ROUND(AVG("Ride Distance"), 2) as avg_distance,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) as pct_of_completed_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Vehicle Type"
ORDER BY avg_fare_per_km DESC