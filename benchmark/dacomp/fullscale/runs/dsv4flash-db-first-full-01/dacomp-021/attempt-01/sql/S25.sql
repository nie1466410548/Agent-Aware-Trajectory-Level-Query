WITH parsed AS (
  SELECT
    CAST(strftime('%w', printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER))) AS INTEGER) AS dow,
    "Vehicle Type" AS vtype,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist,
    "Payment Method" AS pay
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
)
SELECT
  CASE dow WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS weekday,
  ROUND(AVG(dist), 2) AS avg_dist_km,
  ROUND(AVG(value), 2) AS avg_value,
  ROUND(AVG(value / NULLIF(dist, 0)), 2) AS avg_cost_per_km,
  COUNT(*) AS completed_rides,
  ROUND(100.0 * COUNT(*) / SUM(COUNT(*)) OVER (), 2) AS pct_of_completed
FROM parsed
GROUP BY dow
ORDER BY dow