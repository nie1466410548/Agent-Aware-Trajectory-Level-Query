SELECT COUNT(DISTINCT hr."Disaster Reference ID") AS hr_events,
       COUNT(DISTINCT op."Disaster Reference ID") AS op_events,
       COUNT(DISTINCT fin."Disaster Reference ID") AS fin_events,
       COUNT(DISTINCT sup."Disaster Reference ID") AS sup_events,
       COUNT(DISTINCT hub."Disaster Event Reference ID") AS hub_events,
       COUNT(DISTINCT tr."Disaster Reference ID") AS tr_events
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN operations1 op ON op."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'