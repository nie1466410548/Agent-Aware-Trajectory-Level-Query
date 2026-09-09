SELECT 
  COUNT(*) AS n,
  ROUND(AVG("Center Capacity (tons)"),0) AS avg_capacity,
  ROUND(AVG("Utilization (%)"),1) AS avg_util,
  ROUND(AVG("Storage Capacity (m³)"),0) AS avg_storage_m3,
  ROUND(AVG("Available Capacity (m³)"),0) AS avg_avail_m3,
  ROUND(AVG("Inventory Accuracy (%)"),1) AS avg_inv_accuracy,
  ROUND(AVG("Inventory Turnover Rate"),2) AS avg_turnover,
  SUM(CASE WHEN "Warehouse Status"='Excellent' THEN 1 ELSE 0 END) AS wh_excellent,
  SUM(CASE WHEN "Warehouse Status"='Good' THEN 1 ELSE 0 END) AS wh_good,
  SUM(CASE WHEN "Warehouse Status"='Fair' THEN 1 ELSE 0 END) AS wh_fair,
  SUM(CASE WHEN "Warehouse Status"='Poor' THEN 1 ELSE 0 END) AS wh_poor
FROM distribution_hubs hub JOIN disaster_events de ON de."Disaster Event ID" = hub."Disaster Event Reference ID"
WHERE de."Disaster Severity Level" = 'Level 5'