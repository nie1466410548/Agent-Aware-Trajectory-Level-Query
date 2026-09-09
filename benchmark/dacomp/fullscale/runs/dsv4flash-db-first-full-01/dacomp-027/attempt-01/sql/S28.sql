
SELECT c."Secincident Count", c."Safety Ranking", c."Accesslimitation", c."coordeffectlvl",
       c."infosharingstate", c."monitoringfreq", c."evaluationstage", c."lessonslearnedstage",
       c."contingencyplanstage", c."riskmitigationsteps", c."insurancescope", c."compliancestate",
       c."auditstate", c."qualitycontrolsteps", c."mediacoversentiment", c."documentationstate",
       o."Response Phase", o."Operation Status", o."Emergency Level", o."Priority", o."Resource Allocation Status", o."Supply Flow Status",
       d."Disaster Level", d."Disaster Type"
FROM coordination_and_evaluation c
JOIN operations1 o ON o."Disaster Reference ID"=c."Distribution Reference ID"
JOIN disaster_events d ON d."Disaster Event ID"=c."Distribution Reference ID"
