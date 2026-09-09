SELECT 
  u."Age group",
  ROUND(AVG(m."Event Feedback Rating"),3) as avg_rating,
  ROUND(100.0*SUM(CASE WHEN m."Is Event Blocked"='Yes' THEN 1 ELSE 0 END)/COUNT(*),2) as blocked_pct,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),2) as used_pct,
  COUNT(*) as interactions
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"