SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.medical')*1.0 / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)*100),1) AS medical_pct_of_staff,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.volunteers')*1.0 / NULLIF(json_extract(hr."Staffing", '$.personnel.total'),0)),1) AS volunteer_ratio,
  ROUND(AVG(CAST(json_extract(de."Impact Indicator", '$.population.injured') AS REAL) / NULLIF(json_extract(hr."Staffing", '$.personnel.medical'),0)),1) AS injured_per_medic,
  ROUND(AVG(fin."costbene(USD)"*1.0 / NULLIF(fin."budgetallot(USD)",0)),4) AS roi_ratio,
  ROUND(AVG((fin."transportcosts(USD)"+fin."storagecosts(USD)"+fin."personnelcosts(USD)"+fin."opscosts(USD)")*1.0 / NULLIF(fin."budgetallot(USD)",0)*100),1) AS ops_cost_pct_of_budget,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_delivery_time,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS delivery_success_rate,
  ROUND(AVG(tr."Daily Transport Volume (tons)"*1.0 / NULLIF(tr."Number of Vehicles",0)),1) AS tons_per_vehicle_per_day
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity