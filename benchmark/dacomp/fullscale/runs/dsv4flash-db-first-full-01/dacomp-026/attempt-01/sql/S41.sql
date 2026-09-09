SELECT 
  op."Resource Allocation Status",
  ROUND(AVG(tr."Delivery Success Rate"),1) AS avg_deliv_success,
  ROUND(AVG(tr."Average Delivery Time"),1) AS avg_deliv_time,
  ROUND(AVG(hub."Utilization (%)"),1) AS avg_hub_util,
  ROUND(AVG(fin."fundsutilpct(%)"),1) AS avg_fundsutil
FROM operations1 op 
JOIN disaster_events de ON de."Disaster Event ID" = op."Disaster Reference ID"
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID" = de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID" = de."Disaster Event ID"
LEFT JOIN financials1 fin ON fin."Disaster Reference ID" = de."Disaster Event ID"
WHERE de."Disaster Severity Level" = 'Level 5'
GROUP BY op."Resource Allocation Status"
ORDER BY op."Resource Allocation Status"