SELECT planned_timing, 
       ROUND(AVG(email_open_rate), 4) AS avg_open,
       ROUND(AVG(email_click_to_open_rate), 4) AS avg_ctor,
       ROUND(AVG(total_placed_orders), 1) AS avg_orders,
       ROUND(AVG(gmv_net), 1) AS avg_gmv,
       COUNT(*) AS n
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
    email_open_rate, email_click_to_open_rate, total_placed_orders, gmv_net
  FROM klaviyo__campaigns
)
GROUP BY planned_timing
ORDER BY avg_open DESC