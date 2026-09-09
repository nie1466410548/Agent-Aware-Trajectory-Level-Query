SELECT MIN("Customer Technical Assistance Time") as min_ctat,
       MAX("Customer Technical Assistance Time") as max_ctat,
       ROUND(AVG("Customer Technical Assistance Time"),2) as avg_ctat
FROM sheet1 WHERE "Booking Status" = 'Completed'