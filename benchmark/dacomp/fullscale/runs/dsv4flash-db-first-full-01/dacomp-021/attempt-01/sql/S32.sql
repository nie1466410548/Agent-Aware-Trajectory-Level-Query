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
),
daily_agg AS (
  SELECT date_key,
    COUNT(*) AS bookings,
    ROUND(100.0*SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END)/COUNT(*),2) AS cancel_pct,
    ROUND(AVG(CASE WHEN status='Completed' AND dist>0 THEN value/dist END),2) AS cost_per_km
  FROM parsed
  GROUP BY date_key
)
SELECT date_key,
  CASE CAST(strftime('%w', date_key) AS INTEGER)
    WHEN 0 THEN 'Sun' WHEN 1 THEN 'Mon' WHEN 2 THEN 'Tue' WHEN 3 THEN 'Wed'
    WHEN 4 THEN 'Thu' WHEN 5 THEN 'Fri' WHEN 6 THEN 'Sat' END AS dow,
  bookings, cancel_pct, cost_per_km
FROM daily_agg
ORDER BY bookings DESC
LIMIT 10