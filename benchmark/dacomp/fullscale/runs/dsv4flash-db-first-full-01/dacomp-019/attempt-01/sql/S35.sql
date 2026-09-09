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
GROUP BY 1