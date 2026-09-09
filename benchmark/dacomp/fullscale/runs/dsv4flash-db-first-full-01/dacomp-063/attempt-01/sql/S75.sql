-- How many with health > 75 are "Critical Priority - Investigate Contradictions"?
SELECT 
  CASE WHEN overall_health_score > 75 THEN 'health>75' ELSE 'health<=75' END as health_band,
  strategic_priority_recommendation,
  COUNT(*) as cnt
FROM jira__project_risk_assessment
GROUP BY health_band, strategic_priority_recommendation
ORDER BY health_band, cnt DESC