SELECT 
  u."Age group",
  ROUND(100.0 * SUM(m."Number of Shares") / NULLIF(SUM(m."Number of Participants"), 0), 2) as share_rate_pct,
  ROUND(AVG(m."Number of Participants"), 2) as avg_participants,
  ROUND(AVG(m."Number of Shares"), 2) as avg_shares,
  COUNT(m."User ID") as campaign_interactions
FROM user_basic_information_table_1 u
LEFT JOIN marketing_campaign_interaction m ON u."User ID" = m."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"