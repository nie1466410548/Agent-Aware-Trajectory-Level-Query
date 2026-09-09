SELECT is_archived, planned_timing, subject_keyword,
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       COUNT(*) AS n
FROM (
  SELECT
    is_archived,
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
      WHEN SUBJECT LIKE '%故事%' OR SUBJECT LIKE '%品牌%' THEN 'storytelling'
      ELSE 'other'
    END AS subject_keyword,
    email_open_rate, email_click_to_open_rate
  FROM klaviyo__campaigns
)
GROUP BY is_archived, planned_timing, subject_keyword
ORDER BY is_archived, avg_open DESC