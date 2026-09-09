SELECT 
  b."Origin / Tier (Domestic/Imported/JV)" AS origin,
  COUNT(CASE WHEN julianday('2024-12-31') - julianday(i."Last Outbound Date") > 180 THEN 1 END) AS no_outbound_6m,
  COUNT(CASE WHEN julianday('2024-12-31') - julianday(i."Last Inbound Date") > 180 THEN 1 END) AS no_inbound_6m,
  COUNT(CASE WHEN i."Qualified Quantity" = 0 THEN 1 END) AS zero_qualified,
  COUNT(CASE WHEN i."Quarantine Quantity" > 0 THEN 1 END) AS has_quarantine,
  COUNT(*) AS total
FROM basic_drug_information b JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1