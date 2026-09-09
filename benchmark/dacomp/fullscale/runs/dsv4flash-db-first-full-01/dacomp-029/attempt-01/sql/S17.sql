SELECT 
  "New Car Price (incl. tax)" AS np_raw,
  CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np_parsed,
  Mileage,
  CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km','') AS REAL)*10000 
       WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',',''), ' km','') AS REAL)
       ELSE NULL END AS mileage_km,
  CAST(substr("Number of Previous Owners",1,1) AS INTEGER) AS owners
FROM autohome
LIMIT 15