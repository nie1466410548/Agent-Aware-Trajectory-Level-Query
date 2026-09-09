SELECT 
       SUBSTR("Date", 1, 4) || '-' || 
       SUBSTR("Date", 6, INSTR(SUBSTR("Date", 6), '/') - 1) || '-' || 
       SUBSTR("Date", INSTR(SUBSTR("Date", 6), '/') + 6) as formatted_date
FROM sheet1 LIMIT 5