SELECT 
  m."Event Name",
  COUNT(*) as interactions,
  ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
  ROUND(AVG(m."Number of Shares"),1) as avg_shares,
  ROUND(AVG(m."Event Conversion Rate"),2) as avg_conv,
  ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct
FROM marketing_campaign_interaction m
GROUP BY m."Event Name"
ORDER BY interactions DESC