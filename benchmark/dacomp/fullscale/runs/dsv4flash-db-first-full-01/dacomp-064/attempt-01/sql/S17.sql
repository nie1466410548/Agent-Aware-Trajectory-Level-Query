SELECT 
  MIN(engagement_depth_score) AS min_depth, MAX(engagement_depth_score) AS max_depth,
  MIN(engagement_breadth_score) AS min_breadth, MAX(engagement_breadth_score) AS max_breadth,
  MIN(strategic_value_score) AS min_strat, MAX(strategic_value_score) AS max_strat,
  MIN(engagement_quality_score) AS min_qual, MAX(engagement_quality_score) AS max_qual,
  MIN(total_engagement_score) AS min_tot, MAX(total_engagement_score) AS max_tot
FROM jira__stakeholder_engagement_insights