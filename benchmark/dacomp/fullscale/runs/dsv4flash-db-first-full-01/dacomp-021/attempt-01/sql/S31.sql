
WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour,
    "Booking Status" AS status
  FROM sheet1
)
SELECT hour,
  COUNT(*) AS total,
  SUM(CASE WHEN status = 'Cancelled by Customer' THEN 1 ELSE 0 END) AS cust_cancel,
  SUM(CASE WHEN status = 'Cancelled by Driver' THEN 1 ELSE 0 END) AS drv_cancel
FROM parsed
GROUP BY hour
ORDER BY hour
