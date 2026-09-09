
SELECT 
  u."Age group" as age,
  m."Event Name" as evt,
  COUNT(*) as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),1) as avg_dwell,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct
FROM user_basic_information_table_1 u
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", m."Event Name"
