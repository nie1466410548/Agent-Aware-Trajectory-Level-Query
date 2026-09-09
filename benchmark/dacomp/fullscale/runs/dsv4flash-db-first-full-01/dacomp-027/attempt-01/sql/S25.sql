SELECT
 CASE
   WHEN c."Secincident Count" < 33 THEN 'Low (0-32)'
   WHEN c."Secincident Count" < 66 THEN 'Medium (33-65)'
   ELSE 'High (66-100)'
 END AS sec_group,
 ROUND(AVG(o."Estimated Duration (days)"),1) AS avg_duration,
 ROUND(AVG(f."resourcegaps(USD)"),0) AS avg_resourcegap,
 ROUND(AVG(f."fundsutilpct(%)"),1) AS avg_util,
 ROUND(AVG(t."Delivery Success Rate"),1) AS avg_delivery,
 ROUND(AVG(t."Average Delivery Time"),2) AS avg_delivery_time,
 ROUND(AVG(h."Utilization (%)"),1) AS avg_utilization,
 ROUND(AVG(c."stakeholdersatisf"),2) AS avg_stakeholder_sat,
 ROUND(AVG(c."publicperception"),2) AS avg_public_perception,
 ROUND(AVG(c."reportcompliance"),1) AS avg_report_compliance
FROM disaster_events d
JOIN coordination_and_evaluation c ON c."Distribution Reference ID"=d."Disaster Event ID"
JOIN operations1 o ON o."Disaster Reference ID"=d."Disaster Event ID"
JOIN financials1 f ON f."Disaster Reference ID"=d."Disaster Event ID"
JOIN transportation1 t ON t."Disaster Reference ID"=d."Disaster Event ID"
JOIN distribution_hubs h ON h."Disaster Event Reference ID"=d."Disaster Event ID"
GROUP BY sec_group ORDER BY sec_group