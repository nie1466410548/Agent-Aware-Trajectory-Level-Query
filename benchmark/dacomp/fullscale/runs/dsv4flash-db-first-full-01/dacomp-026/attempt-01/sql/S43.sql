SELECT 
  MIN("costbene(USD)") AS min_cb, MAX("costbene(USD)") AS max_cb, ROUND(AVG("costbene(USD)"),1) AS avg_cb,
  MIN("fundsutilpct(%)") AS min_fu, MAX("fundsutilpct(%)") AS max_fu,
  MIN("Delivery Success Rate") AS min_ds, MAX("Delivery Success Rate") AS max_ds,
  MIN("Average Delivery Time") AS min_dt, MAX("Average Delivery Time") AS max_dt,
  MIN("Center Capacity (tons)") AS min_cap, MAX("Center Capacity (tons)") AS max_cap,
  MIN("Utilization (%)") AS min_util, MAX("Utilization (%)") AS max_util
FROM financials1 fin 
JOIN disaster_events de ON de."Disaster Event ID"=fin."Disaster Reference ID"
CROSS JOIN (SELECT 1) 
LEFT JOIN transportation1 tr ON tr."Disaster Reference ID"=de."Disaster Event ID"
LEFT JOIN distribution_hubs hub ON hub."Disaster Event Reference ID"=de."Disaster Event ID"
WHERE de."Disaster Severity Level"='Level 5'