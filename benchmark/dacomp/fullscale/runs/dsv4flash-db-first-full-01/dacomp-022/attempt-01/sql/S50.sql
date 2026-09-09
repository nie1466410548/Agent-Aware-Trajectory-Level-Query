SELECT "Vehicle Type",
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),2) as no_driver_found_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),2) as driver_cancel_rate,
       ROUND(100.0*SUM(CASE WHEN "Booking Status" = 'Incomplete' THEN 1 ELSE 0 END)/COUNT(*),2) as incomplete_rate
FROM sheet1
GROUP BY "Vehicle Type"
ORDER BY no_driver_found_rate DESC