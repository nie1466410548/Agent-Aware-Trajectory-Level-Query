SELECT "Date",
       SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) as formatted
FROM sheet1
WHERE "Booking Status" = 'Completed' AND "Date" = '2024/1/1'
LIMIT 1