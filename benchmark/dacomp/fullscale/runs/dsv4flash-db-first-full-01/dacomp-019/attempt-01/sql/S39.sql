SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 END) AS severe_frozen,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 END) AS severe_scrapped,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Qualified Quantity" = 0 THEN 1 END) AS severe_zero_qualified,
  COUNT(*) AS total
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1