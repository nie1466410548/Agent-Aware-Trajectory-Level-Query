SELECT DISTINCT CAST(SUBSTR("Date", 6, INSTR("Date", '/', 6) - 6) AS INTEGER) as month
FROM sheet1
ORDER BY month