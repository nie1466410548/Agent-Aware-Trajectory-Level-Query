-- Verify China row equals sum of province rows for a sample year
SELECT 
  'sheet1' AS src,
  SUM("Surface Water Supply (100 million m³)") AS sum_surface,
  SUM("Groundwater Supply (100 million m³)") AS sum_gw
FROM sheet1
WHERE "Region Name" <> 'China' AND "Year" = 2018
UNION ALL
SELECT 'China_row', "Surface Water Supply (100 million m³)", "Groundwater Supply (100 million m³)"
FROM sheet1 WHERE "Region Name" = 'China' AND "Year" = 2018