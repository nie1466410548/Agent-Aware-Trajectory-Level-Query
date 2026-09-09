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
GROUP BY 1