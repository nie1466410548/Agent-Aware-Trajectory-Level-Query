SELECT 
  u."Age group",
  u."Gender",
  u."Membership Level",
  u."Income level",
  t."Is At-Risk User",
  t."Price Sensitivity",
  t."Spending Power",
  t."Activity Tag",
  t."Browsing Preference Tag",
  t."Purchase Preference Tag",
  t."Category Preference",
  t."Is High-Value User",
  t."Is Potential Conversion User",
  ROUND(AVG(m."Number of Shares"),2) as avg_shares,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
  ROUND(AVG(m."Event Dwell Time"),1) as avg_dwell,
  ROUND(100.0*SUM(CASE WHEN m."Number of Shares">0 THEN 1 ELSE 0 END)/COUNT(m."User ID"),1) as share_interaction_pct,
  COUNT(m."User ID") as interactions
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
LEFT JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."User ID"
ORDER BY u."Age group"