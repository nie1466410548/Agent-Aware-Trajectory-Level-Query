SELECT COUNT(DISTINCT "Customer ID") as unique_customers,
       COUNT(DISTINCT "Booking ID") as unique_bookings,
       COUNT(DISTINCT "Date") as unique_dates
FROM sheet1