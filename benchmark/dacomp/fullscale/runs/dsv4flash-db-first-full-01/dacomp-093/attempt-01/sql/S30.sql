SELECT
  MIN(count_received_email) AS min_val,
  ROUND(AVG(count_received_email), 0) AS mean_val,
  MAX(count_received_email) AS max_val
FROM klaviyo__campaigns