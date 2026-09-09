SELECT CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER) as month,
       COUNT(*) as rides,
       ROUND(AVG("Booking Value"),2) as avg_booking,
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)),2) as fare_per_km,
       ROUND(SUM("Booking Value"),0) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY month
ORDER BY month