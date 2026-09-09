SELECT "Driver Cancellation Reason", COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Cancelled by Driver'
GROUP BY "Driver Cancellation Reason"
ORDER BY cnt DESC