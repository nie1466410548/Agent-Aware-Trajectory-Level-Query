
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS bookings,
  SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END) AS cancellations,
  SUM(CASE WHEN status = 'No Driver Found' THEN 1 ELSE 0 END) AS no_driver,
  SUM(CASE WHEN status = 'Incomplete' THEN 1 ELSE 0 END) AS incomplete,
  SUM(CASE WHEN status = 'Completed' THEN 1 ELSE 0 END) AS completed,
  AVG(CASE WHEN status = 'Completed' AND dist > 0 THEN value / dist END) AS cost_per_km
FROM parsed
GROUP BY hour
ORDER BY hour
