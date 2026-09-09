SELECT "Reason for cancelling by Customer" AS reason, COUNT(*) AS n
FROM sheet1
WHERE "Cancelled Rides by Customer" = 1
GROUP BY reason
ORDER BY n DESC
LIMIT 12