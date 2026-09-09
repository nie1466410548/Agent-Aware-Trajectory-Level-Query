SELECT 
  u."Age group",
  ROUND(100.0*SUM(CASE WHEN u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END)/COUNT(*),1) as sms_sub_pct,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END) as at_risk_subscribed,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Not Subscribed' THEN 1 ELSE 0 END) as at_risk_not_subscribed,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN u."Marketing SMS subscription status"='Subscribed' THEN 1 ELSE 0 END),0),1) as at_risk_pct_subscribed,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' AND u."Marketing SMS subscription status"='Not Subscribed' THEN 1 ELSE 0 END)/NULLIF(SUM(CASE WHEN u."Marketing SMS subscription status"='Not Subscribed' THEN 1 ELSE 0 END),0),1) as at_risk_pct_not_subscribed
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group"
ORDER BY u."Age group"