SELECT 
  CASE WHEN de."Disaster Severity Level"='Level 5' THEN 'Level 5' ELSE 'Non-Level 5' END AS severity,
  COUNT(*) AS n,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.total')),1) AS avg_total_staff,
  ROUND(AVG(json_extract(hr."Staffing", '$.personnel.volunteers')),1) AS avg_volunteers,
  ROUND(AVG(json_extract(hr."Staffing", '$.readiness.availability_percent')),1) AS avg_avail,
  ROUND(SUM(CASE WHEN json_extract(hr."Staffing", '$.readiness.ppe_status')='Critical' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_ppe_critical,
  ROUND(SUM(CASE WHEN json_extract(hr."Staffing", '$.readiness.training_status')='Complete' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_training_complete,
  ROUND(AVG(fin."budgetallot(USD)"),0) AS avg_budget,
  ROUND(AVG(fin."fundsutilpct(%)"),1) AS avg_fundsutil,
  ROUND(AVG(fin."costbene(USD)"),2) AS avg_costbene,
  ROUND(AVG(fin."resourcegaps(USD)"),0) AS avg_gaps,
  ROUND(SUM(CASE WHEN fin."fundingstate"='Critical' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_funding_critical,
  ROUND(AVG(hub."Center Capacity (tons)"),0) AS avg_hub_capacity,
  ROUND(AVG(hub."Utilization (%)"),1) AS avg_hub_util,
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(SUM(CASE WHEN tr."Last-Mile Delivery Status"='Delayed' THEN 1 ELSE 0 END)*100.0/COUNT(*),1) AS pct_delayed
FROM disaster_events de
LEFT JOIN human_resources hr ON hr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
GROUP BY severity