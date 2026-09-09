SELECT * FROM (
  SELECT
    count_received_email,
    total_count_unique_people,
    count_received_email / NULLIF(total_count_unique_people, 0) AS ratio,
    email_open_rate,
    email_click_to_open_rate,
    campaign_name,
    is_archived,
    variation_id,
    NTILE(100) OVER (ORDER BY count_received_email) AS pct
  FROM klaviyo__campaigns
)
WHERE pct >= 98 OR pct <= 2
ORDER BY count_received_email DESC