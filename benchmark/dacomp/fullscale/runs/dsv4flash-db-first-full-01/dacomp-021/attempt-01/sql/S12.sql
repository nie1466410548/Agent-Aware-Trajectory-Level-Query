WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date",6, instr("Date",'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/',6)+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour
  FROM sheet1
)
SELECT hour, COUNT(*) AS bookings
FROM parsed
GROUP BY hour
ORDER BY bookings DESC