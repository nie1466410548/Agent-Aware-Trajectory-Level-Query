SELECT strftime('%Y-%m-%d', SENT_AT) AS send_date, strftime('%w', SENT_AT) AS dow,
       campaign_name, subject_group, email_open_rate, email_click_to_open_rate,
       total_count_unique_people, count_received_email
FROM (
  SELECT SENT_AT, campaign_name,
    CASE 
      WHEN SUBJECT LIKE '%折扣%' THEN 'discount'
      WHEN SUBJECT LIKE '%新品%' THEN 'new_product'
      WHEN SUBJECT LIKE '%故事%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_group,
    email_open_rate, email_click_to_open_rate, total_count_unique_people, count_received_email
  FROM klaviyo__campaigns
  WHERE campaign_name LIKE '%节前%'
)
ORDER BY SENT_AT