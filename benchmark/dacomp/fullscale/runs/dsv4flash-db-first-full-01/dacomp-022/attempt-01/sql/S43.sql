SELECT "Pickup Location",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Pickup Location"
ORDER BY ride_count DESC
LIMIT 20