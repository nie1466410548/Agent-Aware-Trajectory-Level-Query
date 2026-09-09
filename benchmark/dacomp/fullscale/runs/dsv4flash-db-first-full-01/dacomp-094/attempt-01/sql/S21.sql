SELECT 
  COUNT(*) AS n_persons,
  AVG(active_retention_rate_week) AS avg_ret_week,
  AVG(active_retention_rate_month) AS avg_ret_month,
  AVG(email_open_rate) AS avg_email_open,
  MIN(active_retention_rate_week) AS min_ret_week,
  MAX(active_retention_rate_week) AS max_ret_week,
  MIN(active_retention_rate_month) AS min_ret_month,
  MAX(active_retention_rate_month) AS max_ret_month
FROM klaviyo__persons