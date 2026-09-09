-- Avg close time from user_enhanced for target stakeholders (by joining on stakeholder_id = user_id)
SELECT 
  CASE WHEN s.engagement_impact_score >= 3 AND s.cross_functional_projects >= 3 THEN 'Target' ELSE 'Other' END AS group_type,
  COUNT(DISTINCT u.user_id) AS n_users,
  ROUND(AVG(u.avg_close_time_days),2) AS avg_close_time_days,
  ROUND(AVG(u.median_close_time_days),2) AS median_close_time_days,
  ROUND(AVG(u.avg_age_currently_open_days),1) AS avg_open_age_days
FROM jira__user_enhanced u
JOIN jira__stakeholder_engagement_insights s ON u.user_id = s.stakeholder_id
GROUP BY group_type