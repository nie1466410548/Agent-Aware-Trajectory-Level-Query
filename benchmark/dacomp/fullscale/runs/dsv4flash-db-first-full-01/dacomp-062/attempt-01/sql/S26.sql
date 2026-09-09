SELECT COUNT(*) AS total,
       SUM(CASE WHEN stakeholder_id LIKE '%PRO%' THEN 1 ELSE 0 END) AS id_has_pro,
       SUM(CASE WHEN user_display_name LIKE '%PRO%' THEN 1 ELSE 0 END) AS name_has_pro,
       SUM(CASE WHEN stakeholder_archetype LIKE '%PRO%' THEN 1 ELSE 0 END) AS archetype_has_pro,
       SUM(CASE WHEN recommended_engagement_strategy LIKE '%PRO%' THEN 1 ELSE 0 END) AS strategy_has_pro,
       SUM(CASE WHEN development_opportunity LIKE '%PRO%' THEN 1 ELSE 0 END) AS dev_has_pro
FROM jira__stakeholder_engagement_insights