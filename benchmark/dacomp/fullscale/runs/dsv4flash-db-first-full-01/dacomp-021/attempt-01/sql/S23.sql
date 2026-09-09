
WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT date_key,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 4) AS cost_per_km
FROM parsed
GROUP BY date_key
ORDER BY date_key
