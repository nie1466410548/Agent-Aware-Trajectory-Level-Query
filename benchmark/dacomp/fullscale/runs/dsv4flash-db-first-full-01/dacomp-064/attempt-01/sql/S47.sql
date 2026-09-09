-- Strategic value vs depth/breadth mismatch patterns
SELECT 
  CASE 
    WHEN strategic_value_score >= 80 AND engagement_depth_score < 20 THEN 'High Strategic, Low Depth'
    WHEN strategic_value_score >= 80 AND engagement_depth_score >= 20 THEN 'High Strategic, High Depth'
    WHEN strategic_value_score < 80 AND engagement_depth_score < 20 THEN 'Low Strategic, Low Depth'
    ELSE 'Low Strategic, High Depth'
  END AS strategic_depth_bucket,
  COUNT(*) AS n,
  ROUND(AVG(engagement_breadth_score),1) AS avg_breadth,
  ROUND(AVG(total_outbound_influence - total_inbound_influence),2) AS avg_influence_imbalance,
  ROUND(AVG(issues_assigned*1.0/NULLIF(issues_reported,0)),2) AS avg_assign_report_ratio,
  ROUND(AVG(total_engagement_score),2) AS avg_total_score
FROM jira__stakeholder_engagement_insights
WHERE engagement_impact_score >= 3 AND cross_functional_projects >= 3
GROUP BY strategic_depth_bucket
ORDER BY n DESC