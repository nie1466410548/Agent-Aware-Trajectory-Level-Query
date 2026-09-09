SELECT 
  CASE WHEN "Driver Ratings" < 3.5 THEN '3.0-3.4'
       WHEN "Driver Ratings" < 4.0 THEN '3.5-3.9'
       WHEN "Driver Ratings" < 4.5 THEN '4.0-4.4'
       ELSE '4.5-5.0' END as rating_band,
       COUNT(*) as total_bookings,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END)/COUNT(*),1) as completion_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),1) as driver_cancel_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END)/COUNT(*),1) as cust_cancel_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),1) as no_driver_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END)/COUNT(*),1) as incomplete_rate,
       ROUND(AVG("Booking Value"),2) as avg_booking_value
FROM sheet1
WHERE "Driver Ratings" IS NOT NULL
GROUP BY rating_band
ORDER BY MIN("Driver Ratings")