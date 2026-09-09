SELECT "Vehicle Type",
       COUNT(*) as total_bookings,
       SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) as completed,
       SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) as cancelled_by_driver,
       SUM(CASE WHEN "Booking Status" = 'Cancelled by Customer' THEN 1 ELSE 0 END) as cancelled_by_customer,
       SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END) as incomplete,
       SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END) as no_driver_found,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Completed' THEN 1 ELSE 0 END) / COUNT(*), 2) as completion_rate,
       ROUND(100.0 * SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END) / COUNT(*), 2) as driver_cancellation_rate
FROM sheet1
GROUP BY "Vehicle Type"
ORDER BY completion_rate DESC