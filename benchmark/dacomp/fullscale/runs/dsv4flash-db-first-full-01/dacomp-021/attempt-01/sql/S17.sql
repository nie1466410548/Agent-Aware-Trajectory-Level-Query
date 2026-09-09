WITH parsed AS (
  SELECT
    printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER)) AS date_key,
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT
  CASE CAST(strftime('%w', date_key) AS INTEGER)
    WHEN 0 THEN 'Sunday'
    WHEN 1 THEN 'Monday'
    WHEN 2 THEN 'Tuesday'
    WHEN 3 THEN 'Wednesday'
    WHEN 4 THEN 'Thursday'
    WHEN 5 THEN 'Friday'
    WHEN 6 THEN 'Saturday'
  END AS weekday,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  ROUND(100.0 * SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) / COUNT(*), 2) AS cancel_pct,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  ROUND(AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END), 2) AS avg_cost_per_km
FROM parsed
GROUP BY weekday
ORDER BY bookings DESC