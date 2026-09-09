SELECT "Disaster Event ID",
 json_extract("Impact Indicator",'$.damage_level') AS damage_level,
 json_extract("Impact Indicator",'$.communication') AS communication,
 json_extract("Impact Indicator",'$.transportation') AS transportation
FROM disaster_events