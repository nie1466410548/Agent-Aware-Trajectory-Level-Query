SELECT 
  u."Age group",
  t."Is At-Risk User",
  COUNT(m."User ID") as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),2) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),0) as avg_dwell
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
LEFT JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", t."Is At-Risk User"
ORDER BY u."Age group", t."Is At-Risk User"