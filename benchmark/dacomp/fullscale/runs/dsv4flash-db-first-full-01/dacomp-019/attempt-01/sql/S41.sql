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
GROUP BY 1