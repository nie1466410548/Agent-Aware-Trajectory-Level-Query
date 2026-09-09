SELECT 
  MIN(engagement_depth_score) AS min_depth, MAX(engagement_depth_score) AS max_depth,
  MIN(engagement_breadth_score) AS min_breadth, MAX(engagement_breadth_score) AS max_breadth,
  MIN(strategic_value_score) AS min_strat, MAX(strategic_value_score) AS max_strat,
  MIN(avg_close_time_days) AS min_close, MAX(avg_close_time_days) AS max_close
FROM jira__user_enhanced