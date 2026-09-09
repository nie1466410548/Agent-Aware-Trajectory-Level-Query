SELECT CAST(STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR("Date", '/', 6) + 1)) AS INTEGER) as day_of_week,
       COUNT(*) as ride_count,
       ROUND(SUM("Booking Value"), 2) as total_earnings
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY day_of_week
ORDER BY day_of_week