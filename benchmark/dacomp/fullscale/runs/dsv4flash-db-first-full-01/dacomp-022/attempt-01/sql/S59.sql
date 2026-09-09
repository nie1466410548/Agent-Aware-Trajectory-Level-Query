SELECT CAST(SUBSTR("Time", 1, 2) AS INTEGER) as hour,
       COUNT(*) as total_bookings,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),1) as no_driver_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END)/COUNT(*),1) as completion_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),1) as driver_cancel_rate
FROM sheet1
WHERE CAST(SUBSTR("Time", 1, 2) AS INTEGER) >= 12
GROUP BY hour
ORDER BY hour