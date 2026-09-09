SELECT 
  "Resource Allocation Status" AS alloc_status, COUNT(*) AS cnt
FROM operations1 op JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY "Resource Allocation Status" ORDER BY cnt DESC