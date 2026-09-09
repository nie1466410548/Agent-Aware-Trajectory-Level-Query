SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN p."Abnormal Price Fluctuation Flag" = 'Yes' THEN 1 END) AS abnormal_price_cnt,
       COUNT(*) AS total
FROM basic_drug_information b JOIN pricing_system p ON b."Drug ID" = p."Drug ID"
WHERE b."Origin / Tier (Domestic/Imported/JV)" IN ('Imported', 'Joint-venture')
GROUP BY 1