
SELECT u."Age group" as age,
  t."Is At-Risk User" as risk,
  AVG(m."Number of Shares") as avg_shares,
  AVG(m."Event Feedback Rating") as avg_rating,
  AVG(m."Event Conversion Rate") as avg_conv,
  AVG(m."Event Dwell Time") as avg_dwell
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
JOIN marketing_campaign_interaction m ON u."User ID"=m."User ID"
GROUP BY u."Age group", t."Is At-Risk User"
