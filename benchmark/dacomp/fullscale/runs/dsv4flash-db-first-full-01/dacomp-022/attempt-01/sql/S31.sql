SELECT "Date", COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Completed'
  AND STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) IS NULL
GROUP BY "Date"
LIMIT 20