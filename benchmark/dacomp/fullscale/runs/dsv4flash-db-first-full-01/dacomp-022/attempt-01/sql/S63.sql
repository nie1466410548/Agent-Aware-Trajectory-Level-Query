SELECT "Pickup Location" || ' → ' || "Drop Location" as route,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(AVG("Ride Distance"), 2) as avg_distance
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY route
HAVING ride_count >= 100
ORDER BY avg_fare_per_km DESC
LIMIT 15