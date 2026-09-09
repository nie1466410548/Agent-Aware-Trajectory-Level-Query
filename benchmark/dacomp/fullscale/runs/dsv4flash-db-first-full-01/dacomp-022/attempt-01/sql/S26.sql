SELECT 
       CAST(SUBSTR("Date", 1, 4) AS TEXT) || '-' || 
       CAST(SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) AS TEXT) || '-' || 
       CAST(SUBSTR("Date", INSTR("Date", '/', 6) + 1) AS TEXT) as formatted_date
FROM sheet1 LIMIT 5