SELECT
  planned_timing,
  CASE 
    WHEN CAST(strftime('%w', SENT_AT) AS INTEGER) BETWEEN 1 AND 5 THEN 'weekday'
    ELSE 'weekend'
  END AS actual_day_type,
  CASE 
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 6 AND 11 THEN 'morning'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 12 AND 17 THEN 'afternoon'
    WHEN CAST(strftime('%H', SENT_AT) AS INTEGER) BETWEEN 18 AND 23 THEN 'evening'
    ELSE 'night'
  END AS actual_time,
  COUNT(*) AS n,
  ROUND(AVG(email_open_rate), 4) AS avg_open,
  ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor
FROM (
  SELECT
    CASE 
      WHEN campaign_name LIKE '%工作日-上午%' THEN 'weekday_morning'
      WHEN campaign_name LIKE '%工作日-下午%' THEN 'weekday_afternoon'
      WHEN campaign_name LIKE '%工作日-晚间%' THEN 'weekday_evening'
      WHEN campaign_name LIKE '%周末-上午%' THEN 'weekend_morning'
      WHEN campaign_name LIKE '%周末-晚间%' THEN 'weekend_evening'
      WHEN campaign_name LIKE '%节前-下午%' THEN 'pre_holiday_afternoon'
      ELSE 'other'
    END AS planned_timing,
    SENT_AT, email_open_rate, email_click_to_open_rate
  FROM klaviyo__campaigns
)
GROUP BY planned_timing, actual_day_type, actual_time
ORDER BY planned_timing, actual_day_type, actual_time