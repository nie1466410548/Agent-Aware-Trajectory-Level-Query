SELECT "Vehicle Type",
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Ride Distance"),2) as avg_dist,
       ROUND(SUM("Booking Value"),2) as total_earnings,
       COUNT(*) as completed_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY "Vehicle Type"
ORDER BY total_earnings DESC