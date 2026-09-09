WITH sent AS (
  SELECT campaign_id, CAMPAIGN_TYPE, scheduled_to_send_at
  FROM klaviyo__campaigns
  WHERE STATUS = 'SENT'
)
SELECT CAMPAIGN_TYPE, 
       COUNT(*) as n,
       AVG(count_placed_order / NULLIF(total_count_unique_people,0)) as conv_per_person,
       AVG(count_opened_email / NULLIF(total_count_unique_people,0)) as open_per_person,
       AVG(count_clicked_email / NULLIF(total_count_unique_people,0)) as click_per_person
FROM sent
GROUP BY CAMPAIGN_TYPE
ORDER BY conv_per_person DESC