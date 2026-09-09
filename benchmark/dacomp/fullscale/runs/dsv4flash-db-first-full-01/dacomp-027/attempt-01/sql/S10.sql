SELECT "Disaster Event ID",
 json_extract("Impact Indicator", '$.population.affected') AS affected,
 json_extract("Impact Indicator", '$.population.displaced') AS displaced,
 json_extract("Impact Indicator", '$.population.injured') AS injured,
 json_extract("Impact Indicator", '$.population.casualties') AS casualties,
 json_extract("Impact Indicator", '$.population.missing') AS missing,
 json_extract("Impact Indicator", '$.damage_level') AS damage_level,
 json_extract("Impact Indicator", '$.infrastructure.damage_percent') AS damage_pct,
 json_extract("Impact Indicator", '$.infrastructure.power_outage_percent') AS power_pct,
 json_extract("Impact Indicator", '$.infrastructure.water_damage_percent') AS water_pct,
 json_extract("Impact Indicator", '$.communication') AS comm,
 json_extract("Impact Indicator", '$.transportation') AS transp
FROM disaster_events LIMIT 3