SELECT "Vehicle Type",
       ROUND(AVG("Booking Value" / NULLIF("Ride Distance", 0)), 2) as fare_per_km_weekday,
       ROUND(SUM("Booking Value"), 2) as earnings_weekday
FROM sheet1
WHERE "Booking Status" = 'Completed' AND 
  STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) NOT IN ('0','6')
GROUP BY "Vehicle Type"
ORDER BY fare_per_km_weekday DESC