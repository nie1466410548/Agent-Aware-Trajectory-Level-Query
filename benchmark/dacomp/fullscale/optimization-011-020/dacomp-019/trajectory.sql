-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.
PRAGMA temp_store=MEMORY;
BEGIN;

-- S3
SELECT * FROM basic_drug_information LIMIT 5;

-- S4
SELECT * FROM inventory_management LIMIT 5;

-- S5
SELECT * FROM pricing_system LIMIT 5;

-- S6
SELECT COUNT(*) AS total_drugs, COUNT(DISTINCT "Drug ID") AS unique_drugs FROM basic_drug_information;

-- S7
SELECT "Origin / Tier (Domestic/Imported/JV)" AS origin, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1;

-- S8
SELECT COUNT(*) AS total_inv, COUNT(DISTINCT "Drug ID") AS unique_drugs FROM inventory_management;

-- S9
SELECT "Inventory Status (Normal/Frozen/Scrapped)" AS status, COUNT(*) AS cnt FROM inventory_management GROUP BY 1;

-- S10
SELECT "Inventory Alert Status" AS alert, COUNT(*) AS cnt FROM inventory_management GROUP BY 1;

-- S11
SELECT COUNT(*) AS missing_inv FROM basic_drug_information b LEFT JOIN inventory_management i ON b."Drug ID" = i."Drug ID" WHERE i."Drug ID" IS NULL;

-- S12
SELECT COUNT(*) AS missing_price FROM basic_drug_information b LEFT JOIN pricing_system p ON b."Drug ID" = p."Drug ID" WHERE p."Drug ID" IS NULL;

-- S13
SELECT b."Drug ID", COUNT(i."Inventory ID") AS inv_cnt, COUNT(p."Price ID") AS price_cnt FROM basic_drug_information b LEFT JOIN inventory_management i ON b."Drug ID" = i."Drug ID" LEFT JOIN pricing_system p ON b."Drug ID" = p."Drug ID" GROUP BY b."Drug ID" HAVING inv_cnt > 1 OR price_cnt > 1 LIMIT 10;

-- S14
SELECT "Max Inventory Threshold" AS thresh, "Expiry Alert Days" AS alert_days FROM basic_drug_information LIMIT 10;

-- S15
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin, 
       COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) AS problem_status_cnt,
       COUNT(*) AS total_cnt,
       ROUND(100.0 * COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) / COUNT(*), 1) AS pct_problem
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1;

-- S16
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' THEN 1 END) AS severe_cnt,
       COUNT(CASE WHEN i."Inventory Alert Status" = 'Alert' THEN 1 END) AS alert_cnt,
       COUNT(*) AS total_cnt,
       ROUND(100.0 * COUNT(CASE WHEN i."Inventory Alert Status" IN ('Alert', 'Severe') THEN 1 END) / COUNT(*), 1) AS pct_alert
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1;

-- S17
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       ROUND(AVG(i."Near-expiry Quantity"), 1) AS avg_near_expiry,
       ROUND(AVG(i."Expired Quantity"), 1) AS avg_expired,
       ROUND(AVG(i."Damaged Quantity"), 1) AS avg_damaged,
       ROUND(AVG(i."Returned Quantity"), 1) AS avg_returned,
       ROUND(AVG(i."Pest/Mold Damage Quantity"), 1) AS avg_pest_mold,
       ROUND(AVG(i."Rodent Contamination Quantity"), 1) AS avg_rodent,
       ROUND(AVG(i."Air Contamination Quantity"), 1) AS avg_air_contam,
       ROUND(AVG(i."Temp/Humidity Excursion Record"), 1) AS avg_temp_humidity
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1;

-- S18
SELECT i."Drug ID", COUNT(*) AS cnt FROM inventory_management i LEFT JOIN basic_drug_information b ON i."Drug ID" = b."Drug ID" WHERE b."Drug ID" IS NULL GROUP BY i."Drug ID";

-- S19
SELECT i."Drug ID", COUNT(*) AS cnt FROM inventory_management i JOIN basic_drug_information b ON i."Drug ID" = b."Drug ID" GROUP BY i."Drug ID" HAVING COUNT(*) > 1;

-- S20
SELECT MIN("Last Inbound Date") AS min_in, MAX("Last Inbound Date") AS max_in, MIN("Last Outbound Date") AS min_out, MAX("Last Outbound Date") AS max_out FROM inventory_management;

-- S21
SELECT "GSP Certification Status" AS gsp, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1;

-- S22
SELECT "Storage conditions (room temperature/cool/refrigerated)" AS storage, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1;

-- S23
SELECT "Transportation mode (land/cold chain)" AS transport, COUNT(*) AS cnt FROM basic_drug_information GROUP BY 1;

-- S24
SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  ROUND(AVG(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold",0)), 2) AS avg_stock_to_threshold,
  ROUND(MAX(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold",0)), 2) AS max_stock_to_threshold,
  ROUND(AVG(1.0*i."Qualified Quantity" / NULLIF(b."Max Inventory Threshold",0)), 2) AS avg_qualified_to_threshold
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1;

-- S25
SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(CASE WHEN julianday('2024-12-31') - julianday(i."Last Outbound Date") > 180 THEN 1 END) AS no_outbound_6m,
  COUNT(CASE WHEN julianday('2024-12-31') - julianday(i."Last Inbound Date") > 180 THEN 1 END) AS no_inbound_6m,
  COUNT(CASE WHEN i."Qualified Quantity" = 0 THEN 1 END) AS zero_qualified,
  COUNT(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 END) AS has_quarantine,
  COUNT(*) AS total
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1;

-- S26
SELECT "Inventory Discrepancy Rate", COUNT(*) AS cnt FROM inventory_management GROUP BY 1 ORDER BY cnt DESC LIMIT 15;

-- S27
SELECT "Inventory Discrepancy Rate" FROM inventory_management WHERE "Inventory Discrepancy Rate" LIKE '%0.0%' LIMIT 10;

-- S28
SELECT DISTINCT "Inventory Discrepancy Rate" FROM inventory_management ORDER BY 1 LIMIT 10;

-- S29
SELECT b."Drug ID", b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold,
       b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       b."Adverse Reaction Code" AS adr_code,
       b."Contraindication Code" AS ci_code,
       b."Use in Special Populations" AS special_pop,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry,
       i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified,
       i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound,
       i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2,
       i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned,
       i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold,
       i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam,
       i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID";

-- BUILD C1 before S31
CREATE TEMP TABLE "reuse_019_c1" AS
SELECT ROW_NUMBER() OVER () AS "__reuse_ordinal", src.* FROM (
SELECT b."Drug ID" AS drug_id, b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       b."Max Inventory Threshold" AS max_threshold, b."Expiry Alert Days" AS expiry_alert_days,
       b."GSP Certification Status" AS gsp_status,
       b."Storage conditions (room temperature/cool/refrigerated)" AS storage_condition,
       b."Transportation mode (land/cold chain)" AS transport_mode,
       i."Inventory Status (Normal/Frozen/Scrapped)" AS inv_status,
       i."Inventory Alert Status" AS alert_status,
       i."Near-expiry Quantity" AS near_expiry, i."Quarantine Quantity" AS quarantine,
       i."Qualified Quantity" AS qualified, i."Last Inbound Date" AS last_inbound,
       i."Last Outbound Date" AS last_outbound, i."Inventory Discrepancy Rate" AS disc_rate,
       i."Near-expiry Quantity.1" AS near_expiry2, i."Expired Quantity" AS expired,
       i."Returned Quantity" AS returned, i."Damaged Quantity" AS damaged,
       i."Pest/Mold Damage Quantity" AS pest_mold, i."Rodent Contamination Quantity" AS rodent,
       i."Air Contamination Quantity" AS air_contam, i."Temp/Humidity Excursion Record" AS temp_humidity
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
ORDER BY b."Origin / Tier (Domestic/Imported/JV)", b."Drug ID"
) AS src;

-- S31
SELECT "drug_id", "origin", "max_threshold", "expiry_alert_days", "gsp_status", "storage_condition", "transport_mode", "inv_status", "alert_status", "near_expiry", "quarantine", "qualified", "last_inbound", "last_outbound", "disc_rate", "near_expiry2", "expired", "returned", "damaged", "pest_mold", "rodent", "air_contam", "temp_humidity" FROM temp."reuse_019_c1" ORDER BY "__reuse_ordinal";

-- S32
SELECT "drug_id", "origin", "max_threshold", "expiry_alert_days", "gsp_status", "storage_condition", "transport_mode", "inv_status", "alert_status", "near_expiry", "quarantine", "qualified", "last_inbound", "last_outbound", "disc_rate", "near_expiry2", "expired", "returned", "damaged", "pest_mold", "rodent", "air_contam", "temp_humidity" FROM temp."reuse_019_c1" ORDER BY "__reuse_ordinal";

-- S33
SELECT "drug_id", "origin", "max_threshold", "expiry_alert_days", "gsp_status", "storage_condition", "transport_mode", "inv_status", "alert_status", "near_expiry", "quarantine", "qualified", "last_inbound", "last_outbound", "disc_rate", "near_expiry2", "expired", "returned", "damaged", "pest_mold", "rodent", "air_contam", "temp_humidity" FROM temp."reuse_019_c1" ORDER BY "__reuse_ordinal";

-- S34
SELECT "drug_id", "origin", "max_threshold", "expiry_alert_days", "gsp_status", "storage_condition", "transport_mode", "inv_status", "alert_status", "near_expiry", "quarantine", "qualified", "last_inbound", "last_outbound", "disc_rate", "near_expiry2", "expired", "returned", "damaged", "pest_mold", "rodent", "air_contam", "temp_humidity" FROM temp."reuse_019_c1" ORDER BY "__reuse_ordinal";

-- S35
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       ROUND(AVG(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity"), 0) AS avg_total_stock,
       ROUND(AVG(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / b."Max Inventory Threshold"), 2) AS avg_stock_ratio,
       ROUND(AVG(i."Near-expiry Quantity"), 0) AS avg_near_expiry,
       ROUND(AVG(i."Expired Quantity"), 0) AS avg_expired,
       ROUND(AVG(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 ELSE 0 END)*100, 1) AS pct_quarantined,
       ROUND(AVG(CASE WHEN i."Qualified Quantity" = 0 THEN 1 ELSE 0 END)*100, 1) AS pct_zero_qualified,
       ROUND(AVG(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 ELSE 0 END)*100, 1) AS pct_frozen,
       ROUND(AVG(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 ELSE 0 END)*100, 1) AS pct_scrapped
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1;

-- S36
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN p."Abnormal Price Fluctuation Flag" = 'Yes' THEN 1 END) AS abnormal_price_cnt,
       COUNT(*) AS total
FROM basic_drug_information b JOIN pricing_system p ON b."Drug ID" = p."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1;

-- S37
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN b."GSP Certification Status" = 'Not certified' THEN 1 END) AS gsp_not_certified,
       COUNT(CASE WHEN b."Storage conditions (room temperature/cool/refrigerated)" = 'Refrigerated' THEN 1 END) AS refrigerated,
       COUNT(CASE WHEN b."Transportation mode (land/cold chain)" = 'Cold-chain' THEN 1 END) AS cold_chain,
       COUNT(*) AS total
FROM basic_drug_information b
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1;

-- S38
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
ORDER BY 1, 2;

-- S39
SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Frozen' THEN 1 END) AS severe_frozen,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Inventory Status (Normal/Frozen/Scrapped)" = 'Scrapped' THEN 1 END) AS severe_scrapped,
  COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' AND i."Qualified Quantity" = 0 THEN 1 END) AS severe_zero_qualified,
  COUNT(*) AS total
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1;

-- S40
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
LIMIT 20;

-- S41
SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(*) AS total_drugs,
       ROUND(AVG(i."Expired Quantity" + i."Damaged Quantity" + i."Returned Quantity" + 
                 i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + 
                 i."Air Contamination Quantity" + i."Temp/Humidity Excursion Record"), 1) AS avg_quality_issues,
       ROUND(AVG(1.0 * (i."Expired Quantity" + i."Damaged Quantity" + i."Returned Quantity" + 
                 i."Pest/Mold Damage Quantity" + i."Rodent Contamination Quantity" + 
                 i."Air Contamination Quantity") / NULLIF(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity", 0) * 100), 2) AS quality_issue_rate
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1;

DROP TABLE temp."reuse_019_c1";
COMMIT;
