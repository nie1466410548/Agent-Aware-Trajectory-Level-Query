SELECT
  campaign_id,
  campaign_name,
  SUBJECT,
  is_archived,
  variation_id,
  SENT_AT,
  total_count_unique_people,
  count_received_email,
  count_opened_email,
  count_clicked_email,
  email_open_rate,
  email_click_to_open_rate,
  count_placed_order,
  count_placed_order / NULLIF(total_count_unique_people, 0) AS order_per_person,
  gmv_net,
  gmv_net / NULLIF(total_count_unique_people, 0) AS gmv_per_person,
  product_view_to_order_rate_campaign,
  active_days,
  total_placed_orders,
  CASE 
    WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
    WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
    WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
    WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
    WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
    WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
    ELSE 'other'
  END AS timing,
  CASE 
    WHEN campaign_name LIKE '%工作日%' THEN 'weekday'
    WHEN campaign_name LIKE '%周末%' THEN 'weekend'
    WHEN campaign_name LIKE '%节前%' THEN 'pre_holiday'
    ELSE 'other'
  END AS day_context,
  CASE 
    WHEN campaign_name LIKE '%-上午%' THEN 'morning'
    WHEN campaign_name LIKE '%-下午%' THEN 'afternoon'
    WHEN campaign_name LIKE '%-晚间%' THEN 'evening'
    ELSE 'other'
  END AS time_of_day,
  CASE 
    WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
    WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
    WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
    ELSE 'other'
  END AS subject_group,
  strftime('%Y-%m', SENT_AT) AS sent_month,
  strftime('%w', SENT_AT) AS dow,
  CAST(strftime('%H', SENT_AT) AS INTEGER) AS hour
FROM klaviyo__campaigns