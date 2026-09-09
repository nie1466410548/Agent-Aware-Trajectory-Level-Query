SELECT
  campaign_id,
  campaign_name,
  SUBJECT,
  is_archived,
  variation_id,
  total_count_unique_people,
  count_received_email,
  count_opened_email,
  count_clicked_email,
  email_open_rate,
  email_click_to_open_rate,
  SENT_AT,
  strftime('%w', SENT_AT) AS dow,
  strftime('%H', SENT_AT) AS hour,
  CASE 
    WHEN CAST(strftime('%w', SENT_AT) AS INTEGER) BETWEEN 1 AND 5 THEN 'weekday'
    WHEN CAST(strftime('%w', SENT_AT) AS INTEGER) IN (0,6) THEN 'weekend'
  END AS actual_day_type,
  CASE 
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 6 AND 11 THEN 'morning'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 12 AND 17 THEN 'afternoon'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 18 AND 23 THEN 'evening'
    ELSE 'night'
  END AS actual_time_of_day,
  active_days,
  total_placed_orders,
  gmv_net,
  product_view_to_order_rate_campaign
FROM klaviyo__campaigns
ORDER BY campaign_id
LIMIT 5