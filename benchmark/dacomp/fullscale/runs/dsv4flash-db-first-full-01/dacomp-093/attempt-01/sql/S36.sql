
  SELECT
    campaign_id, campaign_name, SUBJECT, is_archived, variation_id,
    SENT_AT, total_count_unique_people, count_received_email,
    count_opened_email, count_clicked_email, email_open_rate,
    email_click_to_open_rate, count_placed_order, gmv_net,
    product_view_to_order_rate_campaign, active_days, total_placed_orders,
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
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    strftime('%Y-%m', SENT_AT) AS sent_month
  FROM klaviyo__campaigns
