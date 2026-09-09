SELECT "Reason for cancelling by Customer", COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Cancelled by Customer'
GROUP BY "Reason for cancelling by Customer"
ORDER BY cnt DESC