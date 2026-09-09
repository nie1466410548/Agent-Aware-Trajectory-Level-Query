SELECT
  campaign_id,
  campaign_name,
  SUBJECT,
  CASE 
    WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
    WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
    WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
    WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
    WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
    WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
    ELSE 'other'
  END AS planned_timing,
  CASE 
    WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
    WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
    WHEN SUBJECT LIKE '%品牌%' OR SUBJECT LIKE '%故事%' THEN 'storytelling'
    ELSE 'other'
  END AS subject_keyword,
  SENT_AT,
  strftime('%w', SENT_AT) AS dow,
  strftime('%H', SENT_AT) AS hour,
  is_archived,
  variation_id,
  total_count_unique_people,
  count_received_email,
  email_open_rate,
  email_click_to_open_rate,
  total_placed_orders,
  gmv_net,
  product_view_to_order_rate_campaign,
  active_days
FROM klaviyo__campaigns
ORDER BY campaign_id
LIMIT 10