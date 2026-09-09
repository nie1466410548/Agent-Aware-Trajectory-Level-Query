
SELECT age, evt, interactions, avg_rating, avg_shares, avg_conv, used_pct
FROM (
  SELECT 
    u."Age group" as age,
    m."Event Name" as evt,
    COUNT(*) as interactions,
    ROUND(AVG(m."Event Feedback Rating"),2) as avg_rating,
    ROUND(AVG(m."Number of Shares"),1) as avg_shares,
    ROUND(AVG(m."Event Conversion Rate"),3) as avg_conv,
    ROUND(100.0*SUM(CASE WHEN m."Usage Status"='Used' THEN 1 ELSE 0 END)/COUNT(*),1) as used_pct,
    ROW_NUMBER() OVER (PARTITION BY u."Age group" ORDER BY AVG(m."Event Feedback Rating") DESC) as rn
  FROM user_basic_information_table_1 u
  JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
  GROUP BY u."Age group", m."Event Name"
  HAVING COUNT(*) >= 3
)
WHERE rn <= 3
