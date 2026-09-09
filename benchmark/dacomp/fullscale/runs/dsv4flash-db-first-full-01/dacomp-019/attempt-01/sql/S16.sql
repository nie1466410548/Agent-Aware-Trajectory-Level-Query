SELECT b."Origin / Tier (Domestic/Imported/JV)" AS origin,
       COUNT(CASE WHEN i."Inventory Alert Status" = 'Severe' THEN 1 END) AS severe_cnt,
       COUNT(CASE WHEN i."Inventory Alert Status" = 'Alert' THEN 1 END) AS alert_cnt,
       COUNT(*) AS total_cnt,
       ROUND(100.0 * COUNT(CASE WHEN i."Inventory Alert Status" IN ('Alert', 'Severe') THEN 1 END) / COUNT(*), 1) AS pct_alert
FROM basic_drug_information b
JOIN inventory_management i ON b."Drug ID" = i."Drug ID"
GROUP BY 1