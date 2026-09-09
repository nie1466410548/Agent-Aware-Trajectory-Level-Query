SELECT 
  op."Emergency Level",
  COUNT(*) AS cnt,
  ROUND(AVG(op."Estimated Duration (days)"),0) AS avg_duration
FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY op."Emergency Level"
ORDER BY op."Emergency Level"