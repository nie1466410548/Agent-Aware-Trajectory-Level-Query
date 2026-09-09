SELECT 
       CASE WHEN STRFTIME('%w', SUBSTR("Date", 1, 4) || '-' || 
            SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
            SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6)) IS NULL THEN 'unparsed' ELSE 'parsed' END as parse_status,
       COUNT(*) as cnt
FROM sheet1
WHERE "Booking Status" = 'Completed'
GROUP BY parse_status