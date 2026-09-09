SELECT STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week,
       COUNT(*) as ride_count,
       ROUND(AVG("Booking Value"), 2) as avg_booking_value,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as avg_fare_per_km,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY day_of_week
ORDER BY day_of_week