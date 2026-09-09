SELECT
  ROUND(AVG(CASE WHEN row_num <= CAST(0.25 * total AS INTEGER) THEN count_received_email END), 0) AS p25,
  ROUND(AVG(CASE WHEN row_num <= CAST(0.75 * total AS INTEGER) THEN count_received_email END), 0) AS p75
FROM (
  SELECT count_received_email,
         ROW_NUMBER() OVER (ORDER BY count_received_email) AS row_num,
         COUNT(*) OVER () AS total
  FROM klaviyo__campaigns
)
LIMIT 1