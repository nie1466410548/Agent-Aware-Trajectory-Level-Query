SELECT 
  CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen','Scrapped') AND i."Qualified Quantity" = 0 THEN 'Dual risk (frozen/scrapped + zero qualified)' 
       WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen','Scrapped') THEN 'Status frozen/scrapped'
       WHEN i."Qualified Quantity" = 0 THEN 'Zero qualified only'
       ELSE 'Normal' END AS risk_category,
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(*) AS cnt,
  ROUND(AVG(i."Near-expiry Quantity")) AS avg_near_expiry,
  ROUND(AVG(i."Expired Quantity")) AS avg_expired,
  ROUND(AVG(i."Temp/Humidity Excursion Record"), 1) AS avg_temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1, 2
ORDER BY 1, 2