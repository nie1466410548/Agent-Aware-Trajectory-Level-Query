WITH parsed AS (
  SELECT
    CAST(substr("Time", 1, instr("Time", ':')-1) AS INTEGER) AS hour
  FROM sheet1
)
SELECT hour, COUNT(*) AS bookings
FROM parsed
GROUP BY hour
ORDER BY hour