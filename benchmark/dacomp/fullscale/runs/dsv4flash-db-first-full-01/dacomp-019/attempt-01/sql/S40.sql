SELECT b."Drug ID", b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Manufacturer", b."Registered Trademark",
       b."GSP Certification Status", b."Storage conditions (room temperature/cool/refrigerated)",
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status",
       i."Qualified Quantity", i."Near-expiry Quantity", i."Quarantine Quantity",
       (i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") AS total_stock,
       i."Expired Quantity", i."Damaged Quantity",
       (i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + i."Air Contamination Quantity") AS contamination,
       i."Temp/Humidity Excursion Record",
       i."Last Inbound Date", i."Last Outbound Date"
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
  AND i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped')
  AND i."Qualified Quantity" = 0
ORDER BY i."Expired Quantity" DESC
LIMIT 20