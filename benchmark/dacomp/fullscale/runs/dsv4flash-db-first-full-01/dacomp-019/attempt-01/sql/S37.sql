SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN b."GSP Certification Status" = 'Not certified' THEN 1 END) AS gsp_not_certified,
       COUNT(CASE WHEN b."Storage conditions (room temperature/cool/refrigerated)" = 'Refrigerated' THEN 1 END) AS refrigerated,
       COUNT(CASE WHEN b."Transportation mode (land/cold chain)" = 'Cold-chain' THEN 1 END) AS cold_chain,
       COUNT(*) AS total
FROM basic_drug_information b
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1