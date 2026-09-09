SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin, 
       COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) AS problem_status_cnt,
       COUNT(*) AS total_cnt,
       ROUND(100.0 * COUNT(CASE WHEN i."Inventory Status (Normal/Frozen/Scrapped)" IN ('Frozen', 'Scrapped') THEN 1 END) / COUNT(*), 1) AS pct_problem
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1