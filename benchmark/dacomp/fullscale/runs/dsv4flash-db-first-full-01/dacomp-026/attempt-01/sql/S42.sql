
SELECT de."Disaster Event ID",
  json_extract(de."Impact Indicator", '$.population.affected') AS affected,
  json_extract(de."Impact Indicator", '$.population.displaced') AS displaced,
  json_extract(de."Impact Indicator", '$.population.injured') AS injured,
  json_extract(hr."Staffing", '$.personnel.total') AS staff_total,
  json_extract(hr."Staffing", '$.personnel.medical') AS staff_medical,
  json_extract(hr."Staffing", '$.personnel.logistics') AS staff_logistics,
  json_extract(hr."Staffing", '$.personnel.volunteers') AS volunteers,
  json_extract(hr."Staffing", '$.readiness.availability_percent') AS avail_pct,
  fin."budgetallot(USD)" AS budget,
  fin."fundsutilpct(%)" AS fundsutil,
  fin."costbene(USD)" AS costbene,
  fin."resourcegaps(USD)" AS gaps,
  hub."Utilization (%)" AS hub_util,
  hub."Inventory Accuracy (%)" AS inv_acc,
  tr."Total Transport Volume (tons)" AS transport_vol,
  tr."Daily Transport Volume (tons)" AS daily_vol,
  tr."Average Delivery Time" AS deliv_time,
  tr."Delivery Success Rate" AS deliv_success,
  tr."Number of Distribution Points" AS dist_points,
  tr."Number of Vehicles" AS vehicles,
  sup."Inventory resources" AS inv
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN supplies1 sup ON sup."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
