SELECT "Driver Cancellation Reason" AS reason, COUNT(*) AS n
FROM sheet1
WHERE "Cancelled Rides by Driver" = 1
GROUP BY reason
ORDER BY n DESC
LIMIT 12