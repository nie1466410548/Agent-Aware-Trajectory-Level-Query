SELECT COUNT(*) as rides_per_customer, COUNT(*) as customer_count
FROM (
  SELECT "Customer ID", COUNT(*) as ride_count
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
  GROUP BY "Customer ID"
)
GROUP BY ride_count
ORDER BY ride_count
LIMIT 20