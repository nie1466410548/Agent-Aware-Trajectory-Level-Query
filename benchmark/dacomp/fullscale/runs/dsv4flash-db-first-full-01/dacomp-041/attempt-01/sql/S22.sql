SELECT TRIM(gi."Exhibition Hall Record ID") as hall_id, gi."Daily Visitor Count"
FROM gallery_information gi
WHERE gi."Daily Visitor Count" > 900
ORDER BY gi."Daily Visitor Count" DESC