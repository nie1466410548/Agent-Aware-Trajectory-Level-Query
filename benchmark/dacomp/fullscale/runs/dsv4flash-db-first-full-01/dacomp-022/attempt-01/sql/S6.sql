SELECT COUNT(*) as total_rows, 
       COUNT("Booking Value") as has_value,
       COUNT("Ride Distance") as has_distance,
       COUNT("Driver Ratings") as has_rating
FROM sheet1