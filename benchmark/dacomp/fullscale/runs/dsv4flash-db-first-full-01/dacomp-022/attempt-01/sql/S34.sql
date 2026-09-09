SELECT STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS INTEGER)) || '-' || 
       PRINTF('%02d', CAST(SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) AS INTEGER))) as dow
FROM sheet1
WHERE "Booking Status" = 'Completed' AND "Date" = '2024/1/1'