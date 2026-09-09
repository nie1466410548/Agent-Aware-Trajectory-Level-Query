SELECT
  PERCENTILE_25(count_received_email) OVER() AS p25,
  PERCENTILE_75(count_received_email) OVER() AS p75,
  MIN(count_received_email) OVER() AS min_val,
  MAX(count_received_email) OVER() AS max_val,
  AVG(count_received_email) OVER() AS mean_val
FROM klaviyo__campaigns
LIMIT 1