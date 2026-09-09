SELECT de."Disaster Severity Level", op."Emergency Level", COUNT(*) AS cnt
FROM disaster_events de JOIN operations1 op ON de."Disaster Event ID" = op."Disaster Reference ID"
GROUP BY de."Disaster Severity Level", op."Emergency Level"
ORDER BY de."Disaster Severity Level", op."Emergency Level"