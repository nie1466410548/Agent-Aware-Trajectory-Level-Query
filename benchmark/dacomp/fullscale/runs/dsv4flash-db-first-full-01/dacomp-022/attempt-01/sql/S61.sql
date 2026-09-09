SELECT ROUND(AVG(ride_count),1) as avg_rides_per_customer,
       MIN(ride_count) as min_rides, MAX(ride_count) as max_rides
FROM (
  SELECT "Customer ID", COUNT(*) as ride_count
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
  GROUP BY "Customer ID"
)