SELECT 
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as overall_fare_per_km,
       ROUND(AVG("Booking Value"), 2) as overall_avg_booking,
       ROUND(AVG("Ride Distance"), 2) as overall_avg_distance,
       ROUND(SUM("Booking Value"), 2) as overall_total_earnings,
       COUNT(*) as completed_rides
FROM sheet1
WHERE "Booking Status" = 'Completed'