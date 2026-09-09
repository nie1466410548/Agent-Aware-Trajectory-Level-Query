SELECT MIN("Driver Ratings") as min_r, MAX("Driver Ratings") as max_r,
       ROUND(AVG("Driver Ratings"),2) as avg_r,
       MIN("Booking Value") as min_bv, MAX("Booking Value") as max_bv,
       MIN("Ride Distance") as min_d, MAX("Ride Distance") as max_d
FROM sheet1 WHERE "Booking Status" = 'Completed'