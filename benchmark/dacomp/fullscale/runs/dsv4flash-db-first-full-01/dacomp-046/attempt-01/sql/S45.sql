SELECT 
  u."Age group",
  u."Income level",
  COUNT(*) as cnt,
  SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END) as at_risk,
  ROUND(100.0*SUM(CASE WHEN t."Is At-Risk User"='Yes' THEN 1 ELSE 0 END)/COUNT(*),1) as at_risk_pct
FROM user_basic_information_table_1 u
JOIN user_tags_table t ON u."User ID"=t."User ID"
GROUP BY u."Age group", u."Income level"
ORDER BY u."Age group", u."Income level"