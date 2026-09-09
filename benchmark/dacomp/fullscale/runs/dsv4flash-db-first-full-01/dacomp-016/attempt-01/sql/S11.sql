SELECT 
  "Year",
  ROUND("Surface Water Supply (100 million m³)" / NULLIF("Groundwater Supply (100 million m³)", 0), 4) AS "Surface_to_Groundwater_Ratio",
  "Surface Water Supply (100 million m³)" AS "Surface",
  "Groundwater Supply (100 million m³)" AS "Groundwater",
  "Total Water Supply (100 million m³)" AS "Total"
FROM sheet1
WHERE "Region Name" = 'China' AND "Year" BETWEEN 2005 AND 2018
ORDER BY "Year"