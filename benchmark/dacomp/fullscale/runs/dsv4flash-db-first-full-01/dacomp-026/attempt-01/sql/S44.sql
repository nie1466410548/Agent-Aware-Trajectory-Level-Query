SELECT 
  COUNT(*) AS n,
  ROUND(AVG("Inventory Accuracy (%)"),1) AS avg_inv_acc,
  SUM(CASE WHEN "Inventory Accuracy (%)" >= 95 THEN 1 ELSE 0 END) AS inv_acc_ge95,
  ROUND(AVG("Available Capacity (m³)"),0) AS avg_avail_m3,
  ROUND(AVG("Cold Storage Capacity (m³)"),0) AS avg_cold_m3,
  ROUND(AVG("Cold Storage Temperature (℃)"),1) AS avg_cold_temp
FROM distribution_hubs hub JOIN disaster_events de ON de."Disaster Event ID" = hub."Disaster Event Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'