
SELECT "Vehicle Type", "Booking Value", "Ride Distance", "Driver Ratings",
       "Pickup Location",
       "Booking Value" / NULLIF("Ride Distance", 0) as fare_per_km,
       STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
            PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as day_of_week
FROM sheet1
WHERE "Booking Status" = 'Completed'
