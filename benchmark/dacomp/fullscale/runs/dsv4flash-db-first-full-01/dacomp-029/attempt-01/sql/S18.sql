SELECT 
  Title,
  Price,
  Price*10000 AS price_yuan,
  CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) AS np_yuan,
  ROUND(Price*10000 / CAST(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE("New Car Price (incl. tax)", ',', ''), ' yuan', ''), ' (variant)', ''), ' (no space)', ''), ' (with space)', ''), ' yuan ', '') AS REAL) * 100, 2) AS retention_pct,
  (julianday("Posting Date") - julianday("Registration Date"))/365.25 AS age_years,
  CASE WHEN Mileage LIKE '%ten thousand km%' THEN CAST(REPLACE(Mileage, ' ten thousand km','') AS REAL)*10000 
       WHEN Mileage LIKE '%km%' THEN CAST(REPLACE(REPLACE(Mileage, ',',''), ' km','') AS REAL)
       ELSE NULL END AS mileage_km,
  CAST(substr("Number of Previous Owners",1,1) AS INTEGER) AS owners,
  "Fuel Type",
  "Vehicle Class",
  "Engine",
  "Transmission",
  "Drivetrain",
  "Color",
  "Tags",
  "Location"
FROM autohome
LIMIT 20