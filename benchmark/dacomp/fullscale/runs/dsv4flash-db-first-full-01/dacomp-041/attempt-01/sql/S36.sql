
SELECT ra.* FROM risk_assessment ra
JOIN gallery_information gi ON TRIM(gi."Exhibition Hall Record ID") = TRIM(ra."Related Gallery References")
WHERE gi."Daily Visitor Count" > 900
