SELECT 
  CASE WHEN "Customer Technical Assistance Time" < 20 THEN '15-20 min'
       WHEN "Customer Technical Assistance Time" < 25 THEN '20-25 min'
       WHEN "Customer Technical Assistance Time" < 30 THEN '25-30 min'
       WHEN "Customer Technical Assistance Time" < 35 THEN '30-35 min'
       ELSE '35+ min' END as assist_band,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value"/NULLIF("Ride Distance",0)),2) as avg_fare_per_km,
       ROUND(AVG("Driver Ratings"),2) as avg_driver_rating
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY assist_band
ORDER BY MIN("Customer Technical Assistance Time")