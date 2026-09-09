SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  ROUND(AVG(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold",0)), 2) AS avg_stock_to_threshold,
  ROUND(MAX(1.0*(i."Qualified Quantity" + i."Near-expiry Quantity" + i."Quarantine Quantity") / NULLIF(b."Max Inventory Threshold",0)), 2) AS max_stock_to_threshold,
  ROUND(AVG(1.0*i."Qualified Quantity" / NULLIF(b."Max Inventory Threshold",0)), 2) AS avg_qualified_to_threshold
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1