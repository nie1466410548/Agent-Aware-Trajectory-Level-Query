-- Best rated campaigns for each age group
SELECT u."Age group", m."Event Name", 
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  COUNT(*) as cnt
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"
HAVING cnt >= 3
ORDER BY u."Age group", avg_rating DESC