-- Same task, same SQLite connection, immutable main database.
-- Successful data SQL only; original failed attempts are not replayed.
-- Offline selection; source queries and metadata remain in manifest.json.

-- S3
SELECT DISTINCT "Region Name" FROM sheet1 ORDER BY "Region Name";

-- S4
SELECT DISTINCT "Year" FROM sheet1 ORDER BY "Year";

-- S5
SELECT DISTINCT "Region Name" FROM economic_indicator_data ORDER BY "Region Name";

-- S6
SELECT DISTINCT "Year" FROM economic_indicator_data ORDER BY "Year";

-- S7
SELECT "Year", "Region Name", "Surface Water Supply (100 million m³)", "Groundwater Supply (100 million m³)", "Total Water Supply (100 million m³)"
FROM sheet1
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year";

-- S8
SELECT "Year", "Region Name", "Urbanization rate (%)"
FROM economic_indicator_data
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year";

-- S9
SELECT DISTINCT "Year" FROM sheet1 WHERE "Region Name" = 'China' ORDER BY "Year";

-- S10
SELECT DISTINCT "Year" FROM economic_indicator_data WHERE "Region Name" = 'China' ORDER BY "Year";

-- S11
SELECT 
  "Year",
  ROUND("Surface Water Supply (100 million m³)" / NULLIF("Groundwater Supply (100 million m³)", 0), 4) AS "Surface_to_Groundwater_Ratio",
  "Surface Water Supply (100 million m³)" AS "Surface",
  "Groundwater Supply (100 million m³)" AS "Groundwater",
  "Total Water Supply (100 million m³)" AS "Total"
FROM sheet1
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year";

-- S12
SELECT 
  w."Year",
  w."Surface Water Supply (100 million m³)" AS Surface_Supply,
  w."Groundwater Supply (100 million m³)" AS Groundwater_Supply,
  w."Surface Water Supply (100 million m³)" / NULLIF(w."Groundwater Supply (100 million m³)", 0) AS Surf_GW_Ratio,
  e."Urbanization rate (%)" AS Urbanization_Rate
FROM sheet1 w
JOIN economic_indicator_data e
  ON w."Year" = e."Year" AND w."Region Name" = e."Region Name"
WHERE w."Region Name" = 'China' AND w."Year" BETWEEN 2005 AND 2018
ORDER BY w."Year";

-- S13
-- Verify China row equals sum of province rows for a sample year
SELECT 
  'sheet1' AS src,
  SUM("Surface Water Supply (100 million m³)") AS sum_surface,
  SUM("Groundwater Supply (100 million m³)") AS sum_gw
FROM sheet1
WHERE "Region Name" <> 'China' AND "Year" = 2018
UNION ALL
SELECT 'China_row', "Surface Water Supply (100 million m³)", "Groundwater Supply (100 million m³)"
FROM sheet1 WHERE "Region Name" = 'China' AND "Year" = 2018;

-- S14
-- Count of rows per region-year combination in each table to confirm one row per region per year
SELECT (SELECT COUNT(*) FROM sheet1) AS sheet1_rows,
       (SELECT COUNT(*) FROM economic_indicator_data) AS econ_rows,
       (SELECT COUNT(DISTINCT "Region Name") FROM sheet1) AS regions_sheet,
       (SELECT COUNT(DISTINCT "Region Name") FROM economic_indicator_data) AS regions_econ;

-- S15
-- Check if other regions have the same urbanization pattern
SELECT "Region Name", "Year", "Urbanization rate (%)"
FROM economic_indicator_data
WHERE "Region Name" IN ('Beijing Municipality', 'Shanghai Municipality', 'Guangdong Province', 'Hebei Province')
  AND "Year" IN (2005, 2010, 2015, 2018)
ORDER BY "Region Name", "Year";

-- S16
-- Check per capita GDP and industrial value added for China
SELECT "Year", "Per capita GDP (yuan/person)", "Industrial value added (100 million yuan)", "Fixed asset investment (100 million yuan)", "Urbanization rate (%)"
FROM economic_indicator_data
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year";

-- S17
-- Compare China urbanization with mean of provinces (potential aggregation check)
SELECT e."Year",
       (SELECT AVG("Urbanization rate (%)") FROM economic_indicator_data WHERE "Year" = e."Year" AND "Region Name" <> 'China') AS prov_avg_urban,
       MAX(CASE WHEN "Region Name" = 'China' THEN "Urbanization rate (%)" END) AS china_urban
FROM economic_indicator_data e
WHERE e."Year" IN (2005, 2010, 2014, 2018)
GROUP BY e."Year"
ORDER BY e."Year";


