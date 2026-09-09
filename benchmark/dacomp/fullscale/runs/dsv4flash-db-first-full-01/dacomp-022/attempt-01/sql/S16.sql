SELECT "Payment Method",
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Payment Method"
ORDER BY ride_count DESC