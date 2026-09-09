WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status,
    "Booking Value" AS value,
    "Ride Distance" AS dist,
    "Cancelled Rides by Customer" AS cc,
    "Cancelled Rides by Driver" AS cd
  FROM sheet1
)
SELECT
  CASE
    WHEN hour BETWEEN 0 AND 4 THEN 'Late-night trough (0-4)'
    WHEN hour BETWEEN 5 AND 8 THEN 'Early morning (5-8)'
    WHEN hour BETWEEN 9 AND 11 THEN 'Morning peak (9-11)'
    WHEN hour BETWEEN 12 AND 14 THEN 'Midday dip (12-14)'
    WHEN hour BETWEEN 15 AND 16 THEN 'Late afternoon (15-16)'
    WHEN hour BETWEEN 17 AND 20 THEN 'Evening peak (17-20)'
    ELSE 'Late evening (21-23)'
  END AS period,
  COUNT(*) AS bookings,
  ROUND(100.0*SUM(CASE WHEN status IN ('Cancelled by Customer','Cancelled by Driver') THEN 1 ELSE 0 END)/COUNT(*),2) AS cancel_pct,
  ROUND(100.0*SUM(CASE WHEN status='Cancelled by Customer' THEN 1 ELSE 0 END)/COUNT(*),2) AS cust_cancel_pct,
  ROUND(100.0*SUM(CASE WHEN status='Cancelled by Driver' THEN 1 ELSE 0 END)/COUNT(*),2) AS drv_cancel_pct,
  ROUND(100.0*SUM(CASE WHEN status='No Driver Found' THEN 1 ELSE 0 END)/COUNT(*),2) AS no_driver_pct,
  ROUND(100.0*SUM(CASE WHEN status='Incomplete' THEN 1 ELSE 0 END)/COUNT(*),2) AS incomplete_pct,
  ROUND(AVG(CASE WHEN status='Completed' AND dist>0 THEN value/dist END),2) AS cost_per_km
FROM parsed
GROUP BY period
ORDER BY MIN(hour)