
SELECT 
  u."Age group" as age,
  ROUND(100.0*SUM(m."Number of Shares")/NULLIF(SUM(m."Number of Participants"),0),3) as share_rate,
  ROUND(AVG(m."Number of Shares"),2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(100.0*SUM(CASE WHEN m."Is Event Blocked"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as blocked_pct,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct,
  COUNT(*) as interactions
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"
