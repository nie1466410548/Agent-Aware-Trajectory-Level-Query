SELECT
  CASE 
    WHEN count_received_email < 100 THEN 'low (<100)'
    WHEN count_received_email < 150 THEN 'medium (100-150)'
    ELSE 'high (150+)'
  END AS email_volume_group,
  COUNT(*) AS n,
  ROUND(AVG(active_retention_rate_week), 4) AS avg_ret_week,
  ROUND(AVG(active_retention_rate_month), 4) AS avg_ret_month,
  ROUND(AVG(email_open_rate), 4) AS avg_open_rate
FROM klaviyo__persons
GROUP BY 1
ORDER BY AVG(active_retention_rate_week) DESC