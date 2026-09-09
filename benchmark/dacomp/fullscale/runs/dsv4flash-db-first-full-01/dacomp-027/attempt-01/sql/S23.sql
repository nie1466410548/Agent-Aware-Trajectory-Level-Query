SELECT d."Disaster Level",
 ROUND(AVG(o."Estimated Duration (days)"),1) AS avg_duration,
 ROUND(AVG(f."resourcegaps(USD)"),0) AS avg_resourcegap,
 ROUND(AVG(f."fundsutilpct(%)"),1) AS avg_util,
 ROUND(AVG(f."costbene(USD)"),0) AS avg_costbene,
 ROUND(AVG(t."Delivery Success Rate"),1) AS avg_delivery,
 ROUND(AVG(t."Average Delivery Time"),2) AS avg_delivery_time,
 ROUND(AVG(h."Utilization (%)"),1) AS avg_utilization
FROM disaster_events d
JOIN operations1 o ON o."Disaster Reference ID"=d."Disaster Event ID"
JOIN financials1 f ON f."Disaster Reference ID"=d."Disaster Event ID"
JOIN transportation1 t ON t."Disaster Reference ID"=d."Disaster Event ID"
JOIN distribution_hubs h ON h."Disaster Event Reference ID"=d."Disaster Event ID"
GROUP BY d."Disaster Level" ORDER BY d."Disaster Level"