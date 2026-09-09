SELECT ROUND(AVG("Booking Value"),2) as avg_bv, ROUND(AVG("Ride Distance"),2) as avg_dist
FROM sheet1 WHERE "Booking Status" = 'Completed' AND "Ride Distance" <= 5