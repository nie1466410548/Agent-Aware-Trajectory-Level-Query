SELECT
  ROUND(AVG(count_received_email), 0) AS avg_received,
  ROUND(AVG(total_count_unique_people), 0) AS avg_audience,
  ROUND(AVG(count_received_email) / NULLIF(AVG(total_count_unique_people), 0), 2) AS received_ratio,
  MIN(count_received_email) AS min_rec,
  MAX(count_received_email) AS max_rec,
  AVG(email_open_rate) AS avg_open,
  AVG(email_click_to_open_rate) AS avg_ctor
FROM klaviyo__campaigns