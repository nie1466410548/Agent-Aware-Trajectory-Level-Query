WITH parsed AS (
  SELECT
    CAST(strftime('%w', printf('%04d-%02d-%02d',
           CAST(substr("Date",1,4) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+1, instr(substr("Date", instr("Date",'/')+1),'/')-1) AS INTEGER),
           CAST(substr("Date", instr("Date",'/')+instr(substr("Date", instr("Date",'/')+1),'/')+1) AS INTEGER))) AS INTEGER) AS dow,
    "Vehicle Type" AS vtype,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist
  FROM sheet1
  WHERE "Booking Status" = 'Completed'
)
SELECT
  CASE dow WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed' WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS weekday,
  vtype,
  COUNT(*) AS n,
  ROUND(AVG(dist), 2) AS avg_dist,
  ROUND(AVG(value / NULLIF(dist, 0)), 2) AS avg_cost_per_km
FROM parsed
GROUP BY dow, vtype
ORDER BY dow, n DESC